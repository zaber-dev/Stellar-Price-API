# Stellar Price API

A lightweight API that provides real-time price data for a Stellar token in both XLM and USD.

## Features

- Fetches live token prices from the Stellar DEX (Decentralized Exchange)
- Calculates price using both recent trades and liquidity pool data
- Converts token price to USD using current XLM/USD exchange rates
- Provides a simple REST API endpoint to access the pricing data

## Installation

1. Clone the repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

Create a `.env` file in the project root with the following variables:

```
TOKEN_CODE=OVRL
TOKEN_ISSUER=GBZH36ATUXJZKFRMQTAAW42MWNM34SOA4N6E7DQ62V3G5NVITC3QOVRL
```

Replace OVRL and the issuer address with your own token details if needed.

## Usage

Start the server:
```python main.py```

The API will be available at `http://localhost:5000/`

### API Endpoints

- `GET /`: Returns the current token price in both XLM and USD

Example Response:
```json
{
  "xlm": "0.0123456",
  "usd": "0.0012345"
}
```
### License
MIT