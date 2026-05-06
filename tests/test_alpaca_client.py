import pytest
from unittest.mock import Mock, MagicMock, patch
from decimal import Decimal
from trading_client import TradingClient
from trading_client.models import Position, Trade, Account
from trading_client.exceptions import InsufficientBuyingPower, PositionNotFound, InvalidSymbol


class TestBuyOperations:
    """Test buy operations by shares and dollar amount."""

    def test_buy_shares_whole_number(self, mock_alpaca_client):
        """Buy exact number of whole shares."""
        client = mock_alpaca_client
        trade = client.buy_shares("AAPL", 5, dry_run=False)

        assert trade.symbol == "AAPL"
        assert trade.qty == 5
        assert trade.action == "buy"
        assert trade.status == "EXECUTED"

    def test_buy_shares_fractional(self, mock_alpaca_client):
        """Buy fractional shares."""
        client = mock_alpaca_client
        trade = client.buy_shares("AAPL", 2.5, dry_run=False)

        assert trade.symbol == "AAPL"
        assert Decimal(str(trade.qty)) == Decimal("2.5")
        assert trade.action == "buy"

    def test_buy_dollars(self, mock_alpaca_client):
        """Buy stock by dollar amount."""
        client = mock_alpaca_client
        trade = client.buy_dollars("AAPL", 1000, dry_run=False)

        assert trade.symbol == "AAPL"
        assert trade.amount == 1000
        assert trade.action == "buy"

    def test_buy_dry_run_no_api_call(self, mock_alpaca_client, mock_requests):
        """Dry-run mode doesn't call Alpaca API."""
        client = mock_alpaca_client
        trade = client.buy_shares("AAPL", 5, dry_run=True)

        assert trade.status == "SIMULATED"
        # Verify no POST calls made to Alpaca
        mock_requests.post.assert_not_called()

    def test_buy_default_dry_run(self, mock_alpaca_client, mock_requests):
        """By default, trades are dry-run."""
        client = mock_alpaca_client
        trade = client.buy_shares("AAPL", 5)  # No dry_run param

        assert trade.status == "SIMULATED"
        mock_requests.post.assert_not_called()

    def test_buy_insufficient_buying_power(self, mock_alpaca_client):
        """Raise error if insufficient buying power."""
        client = mock_alpaca_client

        with pytest.raises(InsufficientBuyingPower):
            client.buy_dollars("AAPL", 1000000, dry_run=False)

    def test_buy_invalid_symbol(self, mock_alpaca_client):
        """Raise error for invalid symbol."""
        client = mock_alpaca_client

        with pytest.raises(InvalidSymbol):
            client.buy_shares("INVALID_SYMBOL", 5, dry_run=False)


class TestSellOperations:
    """Test sell operations by shares and percent."""

    def test_sell_shares(self, mock_alpaca_client):
        """Sell exact number of shares."""
        client = mock_alpaca_client
        trade = client.sell_shares("AAPL", 3, dry_run=False)

        assert trade.symbol == "AAPL"
        assert trade.qty == 3
        assert trade.action == "sell"
        assert trade.status == "EXECUTED"

    def test_sell_fractional(self, mock_alpaca_client):
        """Sell fractional shares."""
        client = mock_alpaca_client
        trade = client.sell_shares("AAPL", 1.5, dry_run=False)

        assert Decimal(str(trade.qty)) == Decimal("1.5")

    def test_sell_percent_of_position(self, mock_alpaca_client):
        """Sell percentage of current position."""
        client = mock_alpaca_client
        trade = client.sell_percent("AAPL", 50, dry_run=False)

        assert trade.action == "sell"
        assert trade.symbol == "AAPL"

    def test_sell_insufficient_shares(self, mock_alpaca_client):
        """Raise error if selling more than position holds."""
        client = mock_alpaca_client

        with pytest.raises(InsufficientBuyingPower):
            # Try to sell 1000 shares when position is only 10
            client.sell_shares("AAPL", 1000, dry_run=False)

    def test_sell_dry_run(self, mock_alpaca_client, mock_requests):
        """Dry-run sell doesn't call API."""
        client = mock_alpaca_client
        trade = client.sell_shares("AAPL", 2, dry_run=True)

        assert trade.status == "SIMULATED"
        mock_requests.post.assert_not_called()


class TestQueryOperations:
    """Test reading account and position data."""

    def test_get_positions(self, mock_alpaca_client):
        """Get list of all positions."""
        client = mock_alpaca_client
        positions = client.get_positions()

        assert len(positions) > 0
        assert all(isinstance(p, Position) for p in positions)

    def test_get_position_exists(self, mock_alpaca_client):
        """Get specific position that exists."""
        client = mock_alpaca_client
        position = client.get_position("AAPL")

        assert position.symbol == "AAPL"
        assert isinstance(position, Position)

    def test_get_position_not_found(self, mock_alpaca_client):
        """Raise error when position doesn't exist."""
        client = mock_alpaca_client

        with pytest.raises(PositionNotFound):
            client.get_position("NONEXISTENT")

    def test_get_account(self, mock_alpaca_client):
        """Get account info."""
        client = mock_alpaca_client
        account = client.get_account()

        assert isinstance(account, Account)
        assert account.buying_power > 0
        assert account.cash >= 0


class TestDryRunMode:
    """Test dry-run mode behavior."""

    def test_trade_logged_as_simulated(self, mock_alpaca_client, temp_logs_dir):
        """Simulated trades logged with SIMULATED status."""
        client = mock_alpaca_client
        trade = client.buy_shares("AAPL", 5, dry_run=True)

        assert trade.status == "SIMULATED"

    def test_trade_logged_as_executed(self, mock_alpaca_client, temp_logs_dir):
        """Real trades logged with EXECUTED status."""
        client = mock_alpaca_client
        trade = client.buy_shares("AAPL", 5, dry_run=False)

        assert trade.status == "EXECUTED"

    def test_all_trades_in_journal(self, mock_alpaca_client, temp_logs_dir):
        """Both simulated and real trades logged."""
        client = mock_alpaca_client
        client.buy_shares("AAPL", 1, dry_run=True)
        client.buy_shares("TSLA", 1, dry_run=False)

        journal = client.get_trade_journal()
        assert len(journal) == 2


class TestTradeModel:
    """Test Trade data structure."""

    def test_trade_creation(self):
        """Create Trade object with all fields."""
        trade = Trade(
            symbol="AAPL",
            action="buy",
            qty=5,
            status="EXECUTED",
            timestamp="2026-05-05T10:30:00Z"
        )

        assert trade.symbol == "AAPL"
        assert trade.qty == 5

    def test_trade_with_dollar_amount(self):
        """Trade can be created with dollar amount instead of qty."""
        trade = Trade(
            symbol="AAPL",
            action="buy",
            amount=1000,
            status="EXECUTED",
            timestamp="2026-05-05T10:30:00Z"
        )

        assert trade.amount == 1000


class TestPositionModel:
    """Test Position data structure."""

    def test_position_creation(self):
        """Create Position object."""
        position = Position(
            symbol="AAPL",
            qty=10,
            market_value=1500,
            avg_entry_price=150
        )

        assert position.symbol == "AAPL"
        assert position.qty == 10


class TestAccountModel:
    """Test Account data structure."""

    def test_account_creation(self):
        """Create Account object."""
        account = Account(
            cash=50000,
            buying_power=100000,
            portfolio_value=150000
        )

        assert account.cash == 50000
        assert account.buying_power == 100000


class TestIntegration:
    """Integration tests for full trading workflow."""

    def test_buy_then_sell_workflow(self, mock_alpaca_client):
        """Complete workflow: check balance, buy, check position, sell."""
        client = mock_alpaca_client

        # Check account
        account_before = client.get_account()
        assert account_before.buying_power > 0

        # Buy shares
        buy_trade = client.buy_shares("AAPL", 5, dry_run=False)
        assert buy_trade.status == "EXECUTED"

        # Check position
        position = client.get_position("AAPL")
        assert position.qty >= 5

        # Sell half
        sell_trade = client.sell_percent("AAPL", 50, dry_run=False)
        assert sell_trade.status == "EXECUTED"
