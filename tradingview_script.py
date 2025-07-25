# Example TradingView scraping or signal logic
import tradingview_ta

def analyze_market(symbol="NIFTY", exchange="NSE"):
    analysis = tradingview_ta.TA_Handler(
        symbol=symbol,
        exchange=exchange,
        screener="india",
        interval=tradingview_ta.Interval.INTERVAL_15_MIN,
        timeout=10
    )

    summary = analysis.get_analysis().summary
    return {
        "symbol": symbol,
        "signal": summary["RECOMMENDATION"],
        "buy": summary["BUY"],
        "sell": summary["SELL"],
        "neutral": summary["NEUTRAL"]
    }
