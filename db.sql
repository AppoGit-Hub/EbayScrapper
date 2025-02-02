DROP TABLE IF EXISTS Offer;
DROP TABLE IF EXISTS Seller;
DROP TABLE IF EXISTS Category;
DROP TABLE IF EXISTS OfferHistory;
DROP TABLE IF EXISTS SellerHistory;

CREATE TABLE Category (
    name VARCHAR,
    PRIMARY KEY (name)
);

CREATE TABLE Seller (
    pseudo VARCHAR,
    PRIMARY KEY (pseudo)
);

CREATE TABLE SellerHistory (
    date DATE NOT NULL,
    sales_count INT NOT NULL,
    satisfaction DECIMAL NOT NULL,

    PRIMARY KEY (date, seller),
    FOREIGN KEY (pseudo) REFERENCES seller(pseudo),
);

CREATE TABLE Offer (
    title VARCHAR NOT NULL,
    subtitle VARCHAR NULL,
    shipping VARCHAR NULL,
    country VARCHAR NULL,

    seller VARCHAR NOT NULL,
    type VARCHAR NOT NULL,  

    PRIMARY KEY (title, seller),
    FOREIGN KEY (seller) REFERENCES seller(pseudo),
    FOREIGN KEY (type) REFERENCES category(name)
);

CREATE TABLE OfferHistory (
    date DATE NOT NULL,
    star DECIMAL NULL,
    price DECIMAL NULL,
    bid_count INTEGER NULL,

    title VARCHAR NOT NULL,
    seller VARCHAR NOT NULL,

    PRIMARY KEY (date, seller),
    FOREIGN KEY (title, seller) REFERENCES offer(title, seller)
);