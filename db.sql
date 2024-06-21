DROP TABLE IF EXISTS offer;
CREATE TABLE offer (
    id VARCHAR,
    date DATE,
    title VARCHAR,
    type VARCHAR,
    is_new VARCHAR NULL,
    star DECIMAL NULL,
    subtitle VARCHAR NULL,
    price DECIMAL NULL,
    pseudo VARCHAR NULL,
    sales_count INTEGER NULL,
    satisfaction DECIMAL NULL,
    bid_count INTEGER NULL,
    purchase VARCHAR NULL,
    shipping VARCHAR NULL,
    country VARCHAR NULL,
    CONSTRAINT pk_offer PRIMARY KEY (id, date, title, type)
);