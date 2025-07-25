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

        from tradingview_ta import TA_Handler, Interval

def analyze_market(symbol="NIFTY", exchange="NSE"):
    handler = TA_Handler(
        symbol=symbol,
        exchange=exchange,
        screener="india",
        interval=Interval.INTERVAL_15_MIN,
        timeout=10
    )

    analysis = handler.get_analysis()
    return {
        "symbol": symbol,
        "signal": analysis.summary["RECOMMENDATION"],
        "buy": analysis.summary["BUY"],
        "sell": analysis.summary["SELL"],
        "neutral": analysis.summary["NEUTRAL"],
        "indicators": analysis.indicators
    }
