-- 创建 Users 表
CREATE TABLE Users (
    UserID AUTOINCREMENT PRIMARY KEY,
    Username TEXT(255),
    Password TEXT(255),
    Email TEXT(255)
);

-- 插入 Users 数据
INSERT INTO Users (Username, Password, Email) VALUES ('alice', 'alice123', 'alice@example.com');
INSERT INTO Users (Username, Password, Email) VALUES ('bob', 'bob123', 'bob@example.com');
INSERT INTO Users (Username, Password, Email) VALUES ('charlie', 'charlie123', 'charlie@example.com');

-- 创建 Products 表
CREATE TABLE Products (
    ProductID AUTOINCREMENT PRIMARY KEY,
    ProductName TEXT(255),
    Price CURRENCY,
    Category TEXT(255)
);

-- 插入 Products 数据
INSERT INTO Products (ProductName, Price, Category) VALUES ('Laptop', 1200, 'Electronics');
INSERT INTO Products (ProductName, Price, Category) VALUES ('Smartphone', 800, 'Electronics');
INSERT INTO Products (ProductName, Price, Category) VALUES ('Coffee Mug', 15, 'Household');

-- 创建 Orders 表
CREATE TABLE Orders (
    OrderID AUTOINCREMENT PRIMARY KEY,
    UserID INTEGER,
    ProductID INTEGER,
    Quantity INTEGER,
    OrderDate DATE,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

-- 插入 Orders 数据
INSERT INTO Orders (UserID, ProductID, Quantity, OrderDate) VALUES (1, 1, 1, #2023-01-15#);
INSERT INTO Orders (UserID, ProductID, Quantity, OrderDate) VALUES (1, 3, 2, #2023-01-15#);
INSERT INTO Orders (UserID, ProductID, Quantity, OrderDate) VALUES (2, 2, 1, #2023-01-16#);
