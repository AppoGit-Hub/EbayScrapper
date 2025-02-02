
if __name__ == "__main__":
    import os, sys, json, psycopg2, csv
    #from common import POSTGRESS_CREDENTIAL_FILENAME
    #from ebayscrapper.core.queries import INSERT_QUERY
    #from scrap import notnull, nullable

    postgress_path: str = os.path.abspath(POSTGRESS_CREDENTIAL_FILENAME)
    with open(postgress_path, 'r') as key_file:
        postgress_data: dict = json.loads(key_file.read())

    connection = psycopg2.connect(**postgress_data)
    cursor = connection.cursor()

    filepath: str = sys.argv[1]
    type: str = sys.argv[2]

    try:
        with open(filepath, "r", encoding="UTF-8") as file:
            reader = csv.reader(file)
            next(reader)

            for id, date, is_new, title, star, subtitle, price, pseudo, sales_count, satisfaction, bid_count, purchase, shipping, country in reader:
                id: str = id
                date: str = date[:10].replace("/", "-")
                title: str = title.replace("\'", "_")

                if id == "None" or title == "None":
                    continue

                is_new: str = None if is_new == "None" else is_new 
                star: float = None if star == "-1.0" else float(star)
                subtitle: str = subtitle.replace("\'", "_")
                price: float = price
                pseudo: str = pseudo 
                sales_count: int = sales_count
                satisfaction: int= satisfaction
                bid_count: int = None if bid_count == "-1" else int(bid_count)
                purchase: str = None if purchase == "None" else purchase
                shipping: str = shipping
                country: str = country

                cursor.execute(INSERT_QUERY.format(
                    id = notnull(id),
                    title = notnull(title),
                    type = notnull(type),
                    current_date = notnull(date),
                    is_new = nullable(is_new),
                    star = nullable(star),
                    subtitle = nullable(subtitle),
                    price = nullable(price),
                    pseudo = nullable(pseudo),
                    sales_count = nullable(sales_count),
                    satisfaction = nullable(satisfaction),
                    bid_count = nullable(bid_count),
                    purchase = nullable(purchase),
                    shipping = nullable(shipping),
                    country = nullable(country)
                ))
    
            connection.commit()
    except Exception as error:
        print(error)

    finally:
        if "connection" in locals():
            connection.close()
        if "cursor" in locals():
            cursor.close()


