EXIST_QUERY = """
    SELECT *
    FROM offer
    WHERE id = {id} AND date = {date} AND title = {title} AND type = {type};
"""   

INSERT_QUERY = """
    INSERT INTO offer 
    VALUES (
        {id},
        {current_date},
        {title},
        {type},
        {is_new},
        {star},
        {subtitle},
        {price},
        {pseudo},
        {sales_count},
        {satisfaction},
        {bid_count},
        {purchase},
        {shipping},
        {country}
    );
"""