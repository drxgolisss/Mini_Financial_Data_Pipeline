-- Financial Market Data Platform
-- Table creation scripts for Microsoft SQL Server

-- Drop tables if they exist
IF OBJECT_ID('dbo.market_data', 'U') IS NOT NULL
    DROP TABLE dbo.market_data;
GO

IF OBJECT_ID('dbo.daily_returns', 'U') IS NOT NULL
    DROP TABLE dbo.daily_returns;
GO

IF OBJECT_ID('dbo.price_statistics', 'U') IS NOT NULL
    DROP TABLE dbo.price_statistics;
GO

-- Create market_data table for raw OHLCV data
CREATE TABLE dbo.market_data (
    id INT IDENTITY(1,1) PRIMARY KEY,
    symbol NVARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    open DECIMAL(18,4) NOT NULL,
    high DECIMAL(18,4) NOT NULL,
    low DECIMAL(18,4) NOT NULL,
    close DECIMAL(18,4) NOT NULL,
    volume BIGINT NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    CONSTRAINT UQ_market_data UNIQUE (symbol, date)
);
GO

-- Create daily_returns table for calculated returns
CREATE TABLE dbo.daily_returns (
    id INT IDENTITY(1,1) PRIMARY KEY,
    symbol NVARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    close_price DECIMAL(18,4) NOT NULL,
    daily_return DECIMAL(10,4) NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    CONSTRAINT UQ_daily_returns UNIQUE (symbol, date)
);
GO

-- Create price_statistics table for aggregated analytics
CREATE TABLE dbo.price_statistics (
    id INT IDENTITY(1,1) PRIMARY KEY,
    symbol NVARCHAR(10) NOT NULL,
    latest_date DATE NOT NULL,
    latest_close DECIMAL(18,4) NOT NULL,
    avg_close DECIMAL(18,4) NOT NULL,
    min_close DECIMAL(18,4) NOT NULL,
    max_close DECIMAL(18,4) NOT NULL,
    volatility DECIMAL(18,4) NOT NULL,
    updated_at DATETIME DEFAULT GETDATE(),
    CONSTRAINT UQ_price_statistics UNIQUE (symbol)
);
GO

-- Create index for faster queries
CREATE INDEX IX_market_data_symbol_date 
ON dbo.market_data (symbol, date);
GO

CREATE INDEX IX_daily_returns_symbol_date 
ON dbo.daily_returns (symbol, date);
GO

PRINT 'Tables created successfully';
GO