import unittest
from app.currency_converter import fetch_exchange_rates
from unittest.mock import AsyncMock, patch

class TestFetchExchangeRates(unittest.IsolatedAsyncioTestCase):

    @patch("httpx.AsyncClient.get")
    async def test_fetch_exchange_rates_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "base_code": "EUR",
            "conversion_rates": {"USD": 1.2}
        }

        result = await fetch_exchange_rates({"EUR"})
        self.assertEqual(result, {"EUR": 1.2})
