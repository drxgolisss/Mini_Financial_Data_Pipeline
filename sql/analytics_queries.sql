-- Analytics queries for Financial Market Data Platform
-- Microsoft SQL Server / T-SQL syntax

-- Query 1: Get latest price for each symbol
SELECT 
    symbol,
    MAX(date) AS latest_date,
    close AS latest_close
FROM dbo.market_data
GROUP BY symbol, close
ORDER BY symbol;
GO

-- Query 2: Calculate average close price per symbol
SELECT 
    symbol,
    AVG(close) AS avg_close_price,
    MIN(close) AS min_price,
    MAX(close) AS max_price
FROM dbo.market_data
GROUP BY symbol
ORDER BY symbol;
GO

-- Query 3: Calculate daily returns
SELECT 
    symbol,
    date,
    close,
    LAG(close, 1) OVER (PARTITION BY symbol ORDER BY date) AS prev_close,
    ((close - LAG(close, 1) OVER (PARTITION BY symbol ORDER BY date)) 
     / LAG(close, 1) OVER (PARTITION BY symbol ORDER BY date)) * 100 AS daily_return_pct
FROM dbo.market_data
ORDER BY symbol, date;
GO

-- Query 4: Calculate volatility (standard deviation of daily returns)
WITH daily_returns AS (
    SELECT 
        symbol,
        date,
        close,
        LAG(close, 1) OVER (PARTITION BY symbol ORDER BY date) AS prev_close
    FROM dbo.market_data
)
SELECT 
    symbol,
    STDEV(((close - prev_close) / prev_close) * 100) AS volatility
FROM daily_returns
WHERE prev_close IS NOT NULL
GROUP BY symbol
ORDER BY symbol;
GO

-- Query 5: Get price statistics summary
SELECT 
    symbol,
    MAX(date) AS latest_date,
    MAX(close) FILTER (WHERE date = MAX(date)) AS latest_close,
    AVG(close) AS avg_close,
    MIN(close) AS min_price,
    MAX(close) AS max_price
FROM dbo.market_data
GROUP BY symbol
ORDER BY symbol;
GO

-- Query 6: Get top 10 days with highest returns
SELECT TOP 10
    symbol,
    date,
    close AS current_close,
    LAG(close, 1) OVER (PARTITION BY symbol ORDER BY date) AS prev_close,
    ((close - LAG(close, 1) OVER (PARTITION BY symbol ORDER BY date)) 
     / LAG(close, 1) OVER (PARTITION BY symbol ORDER BY date)) * 100 AS return_pct
FROM dbo.market_data
ORDER BY return_pct DESC;
GO

-- Query 7: Get data for a specific symbol and date range
SELECT 
    symbol,
    date,
    open,
    high,
    low,
    close,
    volume
FROM dbo.market_data
WHERE symbol = 'AAPL' 
  AND date BETWEEN '2023-01-01' AND '2024-01-01'
ORDER BY date;
GO

PRINT 'Analytics queries created successfully';
GO