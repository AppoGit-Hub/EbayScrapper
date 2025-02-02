INSERT_OFFER = """
    INSERT INTO offer 
    VALUES (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s
    );
"""

EXIST_OFFER = """
    SELECT *
    FROM OFFER
    WHERE ID = %s;
"""   

INSERT_AUTHOR = """
    INSERT INTO AUTHOR (PSEUDO, COUNTRY_ID)
    VALUES (%s, %s)
"""

EXIST_AUTHOR = """
    SELECT *
    FROM AUTHOR
    WHERE PSEUDO = %s;
"""

EXIST_PURCHASECATEGORY = """
    SELECT *
    FROM PURCHASE_CATEGORY
    WHERE NAME = %s;
"""

INSERT_PURCHASECATEGORY = """
    INSERT INTO PURCHASE_CATEGORY
    VALUES (%s)
"""

EXIST_STAR = """
    SELECT * 
    FROM STAR
    WHERE VALUE = %s;
"""

INSERT_STAR = """
    INSERT INTO STAR
    VALUES (%s)
"""

EXIST_COUNTRY = """
    SELECT * 
    FROM COUNTRY
    WHERE NAME = %s;
"""

INSERT_COUNTRY = """
    INSERT INTO COUNTRY
    VALUES (%s)
"""

