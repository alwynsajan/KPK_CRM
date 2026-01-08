-- ===============================
-- Step 1: Create Database
-- ===============================
CREATE DATABASE IF NOT EXISTS KPKdb;
USE KPKdb;

-- ===============================
-- Step 2: Customer Table
-- ===============================
CREATE TABLE IF NOT EXISTS customerData (
    customerID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    customerType VARCHAR(50),
    email VARCHAR(255),
    phone VARCHAR(20),
    address TEXT,
    state VARCHAR(50),
    postcode VARCHAR(10),
    ABN VARCHAR(20)
);

-- ===============================
-- Step 3: Product Table
-- ===============================
CREATE TABLE IF NOT EXISTS productData (
    productID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    productBarCode INT,
    pdtType VARCHAR(100),
    price DECIMAL(10,2) NOT NULL
);

-- ===============================
-- Step 4: Sales Table
-- ===============================
CREATE TABLE IF NOT EXISTS sales (
    saleID INT AUTO_INCREMENT PRIMARY KEY,
    saleDateTime DATETIME NOT NULL,
    customerID INT,
    paymentType VARCHAR(50) NOT NULL,
    note TEXT,

    FOREIGN KEY (customerID)
        REFERENCES customerData(customerID)
        ON DELETE SET NULL
);

-- ===============================
-- Step 5: Sale Items Table
-- ===============================
CREATE TABLE IF NOT EXISTS saleItems (
    saleItemID INT AUTO_INCREMENT PRIMARY KEY,
    saleID INT NOT NULL,
    productName VARCHAR(255) NOT NULL,
    cost DECIMAL(10,2) NOT NULL,
    quantity INT NOT NULL,

    FOREIGN KEY (saleID)
        REFERENCES sales(saleID)
        ON DELETE CASCADE
);

-- ===============================
-- Step 6: Per-Day Sales Summary
-- (Optional but useful for reports)
-- ===============================
CREATE TABLE IF NOT EXISTS perDaySale (
    saleDate DATE PRIMARY KEY,
    totalSales DECIMAL(10,2) NOT NULL
);

-- ===============================
-- Step 7: Verify Tables
-- ===============================
SHOW TABLES;
