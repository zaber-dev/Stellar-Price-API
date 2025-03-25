# Understanding the Stellar Price API

This document explains the technical details of how the Stellar Price API works and the methods used to calculate token prices on the Stellar network.

## Overview

The Stellar Price API fetches and calculates the price of a specific Stellar token in both XLM (native Stellar currency) and USD. It uses two primary sources of price data:

1. Recent trades on the Stellar DEX (Decentralized Exchange)
2. Liquidity pool reserves (AMM - Automated Market Maker)

## Technical Details

### Price Data Sources

#### 1. Stellar DEX Trade Data

The API queries the Stellar Horizon server to get the most recent trade for the token pair (e.g., OVRL/XLM). This provides the most recent market price at which the token was traded:

```python
trades = server.trades().for_asset_pair(
    base=Asset(TOKEN_CODE, TOKEN_ISSUER), 
    counter=Asset.native()
).limit(1).order("desc").call()
```

The price is extracted from the trade record using the price ratio (`n/d`).

#### 2. Liquidity Pool Data (AMM)

Liquidity pools on Stellar provide another source of pricing data. The price of the token in a pool is determined by the ratio of reserves:

```python
pool_response = server.liquidity_pools().for_reserves([token_asset, native_asset]).call()
```

The AMM price is calculated as `XLM_reserves / token_reserves`.

### Price Selection Logic

The API uses the following logic to determine the final price:
- If both trade and AMM prices are available, it uses the AMM price (generally more stable)
- If only one price source is available, it uses that
- If no price data is available, it returns zero

### XLM to USD Conversion

To convert the XLM price to USD, the API fetches the current XLM/USD price from the Kraken exchange API:

```python
response = requests.get("https://api.kraken.com/0/public/Ticker?pair=XLMUSD", timeout=5)
```

Then it multiplies the token's XLM price by the XLM/USD exchange rate.

## Stellar Concepts Used

### Assets

On Stellar, assets are represented by:
- Asset code (e.g., "OVRL")
- Asset issuer (the public key of the account that issued the asset)

Native XLM is a special case that doesn't require an issuer.

### Liquidity Pools

Stellar's liquidity pools allow users to provide liquidity for pairs of assets. The API uses these pools to determine the market price based on the ratio of assets in the pool.

### DEX (Decentralized Exchange)

Stellar has a built-in decentralized exchange where users can place orders to buy or sell assets. The API queries recent trades from this exchange.

## Further Reading

- [Stellar Developer Documentation](https://developers.stellar.org/docs)
- [Stellar SDK for Python](https://stellar-sdk.readthedocs.io/)
- [Understanding Liquidity Pools on Stellar](https://developers.stellar.org/docs/learn/encyclopedia/sdex/liquidity-on-stellar-sdex-liquidity-pools)
