-- POSTGRES

DROP TABLE IF EXISTS SALES_COUNT;
DROP TABLE IF EXISTS BID_COUNT;
DROP TABLE IF EXISTS SATISFACTION;
DROP TABLE IF EXISTS OFFER;
DROP TABLE IF EXISTS STAR;
DROP TABLE IF EXISTS AUTHOR;
DROP TABLE IF EXISTS PURCHASE_CATEGORY;
DROP TABLE IF EXISTS COUNTRY;

CREATE TABLE PURCHASE_CATEGORY (
    NAME VARCHAR NOT NULL,
    PRIMARY KEY (NAME)
);

CREATE TABLE COUNTRY (
    NAME VARCHAR NOT NULL,
    PRIMARY KEY (NAME)
);

CREATE TABLE AUTHOR (
    ID SERIAL NOT NULL,
    PSEUDO VARCHAR NOT NULL,
    COUNTRY_ID VARCHAR,
    PRIMARY KEY (ID),
    FOREIGN KEY (COUNTRY_ID) REFERENCES COUNTRY(NAME)
);

CREATE TABLE SATISFACTION (
    AUTHOR_ID INT NOT NULL,
    "DATE" DATE NOT NULL,
    VALUE DECIMAL NOT NULL,
    PRIMARY KEY (AUTHOR_ID, "DATE"),
    FOREIGN KEY (AUTHOR_ID) REFERENCES AUTHOR(ID)
);

CREATE TABLE BID_COUNT (
    AUTHOR_ID INT NOT NULL,
    "DATE" DATE NOT NULL,
    VALUE INT NOT NULL,
    PRIMARY KEY (AUTHOR_ID, "DATE"),
    FOREIGN KEY (AUTHOR_ID) REFERENCES AUTHOR(ID)
);

CREATE TABLE SALES_COUNT (
    AUTHOR_ID INT NOT NULL,
    "DATE" DATE NOT NULL,
    VALUE INT NOT NULL,
    PRIMARY KEY (AUTHOR_ID, "DATE"),
    FOREIGN KEY (AUTHOR_ID) REFERENCES AUTHOR(ID)
);

CREATE TABLE STAR (
    VALUE DECIMAL NOT NULL,
    PRIMARY KEY (VALUE)
);

CREATE TABLE OFFER (
    ID VARCHAR NOT NULL,
    "DATE" DATE NOT NULL,
    TITLE VARCHAR NOT NULL,
    SUBTITLE VARCHAR,  
    PRICE DECIMAL NOT NULL,
    SHIPPING VARCHAR,
    PURCHASE_ID VARCHAR,
    STAR_ID DECIMAL,
    AUTHOR_ID INT NOT NULL,
    PRIMARY KEY (ID),
    FOREIGN KEY (PURCHASE_ID) REFERENCES PURCHASE_CATEGORY(NAME),
    FOREIGN KEY (STAR_ID) REFERENCES STAR(VALUE),
    FOREIGN KEY (AUTHOR_ID) REFERENCES AUTHOR(ID)
);