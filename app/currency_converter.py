import httpx
import asyncio
import logging
import time
from typing import Dict
from app.config import settings

API_URL = f"https://v6.exchangerate-api.com/v6/{settings.EXCHANGE_API_KEY}/latest/"
MAX_RETRIES = 3  # Max retry attempts
TIMEOUT = 10  # Timeout for each request in seconds
RETRY_DELAY = 2  # Delay between retry attempts (in seconds)

# Default rates for fallback
DEFAULT_RATES = {
    "USD": 1,  # 1 USD to USD
    "EUR": 1.1,  # Example fallback rate
    "INR": 0.013,  # Example fallback rate
}

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def fetch_exchange_rates(currencies: set[str]) -> Dict[str, float]:
    """Fetches exchange rates for the given currencies from the ExchangeRate-API with retries and fallback."""
    rates = {}

    async with httpx.AsyncClient() as client:
        # Create tasks for each currency
        tasks = [fetch_currency_rate_with_retry(client, cur) for cur in currencies]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        for cur, response in zip(currencies, responses):
            if isinstance(response, httpx.Response):
                if response.status_code == 200:
                    data = response.json()
                    usd_rate = data.get("conversion_rates", {}).get("USD")
                    if usd_rate:
                        rates[cur] = usd_rate
                    else:
                        logger.warning(f"No USD rate found for {cur}, using default rate.")
                        rates[cur] = DEFAULT_RATES.get(cur, 1)  # Fallback to default rate if no USD rate
                else:
                    logger.error(f"Failed to fetch data for {cur}. Status code: {response.status_code}")
                    rates[cur] = DEFAULT_RATES.get(cur, 1)  # Fallback on failure
            else:
                logger.error(f"Error fetching {cur}: {response}")
                rates[cur] = DEFAULT_RATES.get(cur, 1)  # Fallback on error

    return rates

async def fetch_currency_rate_with_retry(client: httpx.AsyncClient, currency: str) -> httpx.Response:
    """Fetches exchange rate for a single currency with retry logic."""
    for attempt in range(MAX_RETRIES):
        try:
            response = await client.get(f"{API_URL}{currency}", timeout=TIMEOUT)
            response.raise_for_status()  # Will raise an error for 4xx/5xx status codes
            return response
        except httpx.TimeoutException:
            logger.warning(f"Request for {currency} timed out. Retrying ({attempt + 1}/{MAX_RETRIES})...")
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            logger.error(f"Attempt {attempt + 1}/{MAX_RETRIES} - Error fetching {currency}: {str(e)}")

        if attempt < MAX_RETRIES - 1:
            time.sleep(RETRY_DELAY)  # Wait before retrying
        else:
            logger.error(f"Max retry attempts reached for {currency}. Using fallback rates.")
            return None  # Return None to trigger fallback in the main function

# Function to convert an amount to USD using the exchange rate
def convert_to_usd(amount: float, rate: float) -> float:
    """Converts the given amount to USD using the provided exchange rate."""
    return round(amount * rate, 2)
