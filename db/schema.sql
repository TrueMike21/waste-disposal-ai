-- Run in SQL Server Management Studio
CREATE DATABASE WasteDisposalDB;
GO

USE WasteDisposalDB;
GO

CREATE TABLE PredictionLog (
    id            INT IDENTITY(1,1) PRIMARY KEY,
    timestamp     DATETIME2 DEFAULT GETDATE(),
    predicted_class NVARCHAR(50),
    confidence    FLOAT,
    disposal_category NVARCHAR(100),
    low_confidence BIT,
    image_filename NVARCHAR(255)
);