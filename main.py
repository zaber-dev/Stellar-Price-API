import os
import time
import requests
from flask import Flask, jsonify
from stellar_sdk.server import Server, Asset
from dotenv import load_dotenv
import threading

load_dotenv()
TOKEN_CODE = os.getenv("TOKEN_CODE", "OVRL")
TOKEN_ISSUER = os.getenv("TOKEN_ISSUER", "GBZH36ATUXJZKFRMQTAAW42MWNM34SOA4N6E7DQ62V3G5NVITC3QOVRL")

server = Server(horizon_url="https://horizon.stellar.org")
app = Flask(__name__)
token_price = {"xlm": "0.0000000", "usd": "0.0000000"}

def fetch_price():
    global token_price
    while True:
        try:
            last_trade_price_xlm = 0.0
            amm_price_xlm = 0.0
            
            # Get trade price
            try:
                trades = server.trades().for_asset_pair(
                    base=Asset(TOKEN_CODE, TOKEN_ISSUER), 
                    counter=Asset.native()
                ).limit(1).order("desc").call()
                
                if trades["_embedded"]["records"]:
                    trade = trades["_embedded"]["records"][0]
                    if "price" in trade and "n" in trade["price"] and "d" in trade["price"]:
                        last_trade_price_xlm = float(trade["price"]["n"]) / float(trade["price"]["d"])
            except Exception:
                pass
            
            # Get pool price
            try:
                token_asset = Asset(TOKEN_CODE, TOKEN_ISSUER)
                native_asset = Asset.native()
                
                pool_response = server.liquidity_pools().for_reserves([token_asset, native_asset]).call()
                
                if pool_response["_embedded"]["records"]:
                    for pool in pool_response["_embedded"]["records"]:
                        reserves = pool["reserves"]
                        xlm_amount = 0.0
                        token_amount = 0.0
                        
                        for reserve in reserves:
                            asset_str = reserve["asset"]
                            if asset_str == "native":
                                xlm_amount = float(reserve["amount"])
                            elif TOKEN_CODE in asset_str and TOKEN_ISSUER in asset_str:
                                token_amount = float(reserve["amount"])
                        
                        if xlm_amount > 0 and token_amount > 0:
                            amm_price_xlm = xlm_amount / token_amount
                            break
                else:
                    pool_response = server.liquidity_pools().for_reserves([token_asset]).call()
                    
                    if pool_response["_embedded"]["records"]:
                        for pool in pool_response["_embedded"]["records"]:
                            reserves = pool["reserves"]
                            xlm_amount = 0.0
                            token_amount = 0.0
                            
                            for reserve in reserves:
                                asset_str = reserve["asset"]
                                if asset_str == "native":
                                    xlm_amount = float(reserve["amount"])
                                elif TOKEN_CODE in asset_str and TOKEN_ISSUER in asset_str:
                                    token_amount = float(reserve["amount"])
                            
                            if xlm_amount > 0 and token_amount > 0:
                                amm_price_xlm = xlm_amount / token_amount
                                break
            except Exception:
                pass
            
            # Choose best price
            final_price_xlm = amm_price_xlm if amm_price_xlm > 0 else last_trade_price_xlm
            
            # Get XLM/USD price
            xlm_usd = 0.0
            try:
                response = requests.get("https://api.kraken.com/0/public/Ticker?pair=XLMUSD", timeout=5)
                data = response.json()
                xlm_usd = float(data["result"]["XXLMZUSD"]["c"][0])
            except Exception:
                pass
            
            # Update price
            price_usd = final_price_xlm * xlm_usd
            if final_price_xlm > 0:
                token_price = {"xlm": f"{final_price_xlm:.7f}", "usd": f"{price_usd:.7f}"}
            
        except Exception:
            pass
        
        time.sleep(5)

threading.Thread(target=fetch_price, daemon=True).start()

@app.route("/price", methods=["GET"])
def get_price():
    return jsonify(token_price)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
