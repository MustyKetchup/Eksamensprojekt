

CREATE TABLE Stock (
    ProductID INTEGER PRIMARY KEY ,
    ProductName TEXT NOT NULL,
    Category TEXT NOT NULL,
    Price FLOAT NOT NULL,
    Quantity INTEGER NOT NULL
);

INSERT INTO Stock (ProductID, ProductName, Category, Price, Quantity)
VALUES
    (1, 'Smartphone', 'Elektronik', 2999.99, 5),
    (2, 'Laptop', 'Elektronik', 7999.99, 3),
    (3, 'Kaffemaskine', 'Husholdning', 1499.99, 10),
    (4, 'T-shirt', 'Tøj', 199.99, 20),
    (5, 'Køleskab', 'Husholdning', 4999.99, 2),
    (6, 'Bluetooth Højttaler', 'Elektronik', 899.99, 15),
    (7, 'Løbesko', 'Sport', 799.99, 8),
    (8, 'Bordlampe', 'Husholdning', 299.99, 12),
    (9, 'Kamera', 'Elektronik', 3499.99, 4),
    (10, 'Håndklæde', 'Husholdning', 99.99, 30);


-- Opret User uden FOREIGN KEY først
CREATE TABLE User (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserName TEXT NOT NULL,
    UserPassword TEXT NOT NULL,
    BasketID INTEGER,
    FOREIGN KEY (BasketID) REFERENCES Basket (BasketID)
);

-- Opret Basket
CREATE TABLE Basket (
    BasketID INTEGER PRIMARY KEY AUTOINCREMENT,
    ProductID INTEGER,
    PriceTotal FLOAT,
    ProductQuantity INTEGER,
    UserID INTEGER,
    FOREIGN KEY (ProductID) REFERENCES Stock(ProductID),
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);