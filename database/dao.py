from database.DB_connect import DBConnect
from model.prodotto import Prodotto
from model.vendita import Vendita
class DAO:
    @staticmethod
    def get_date_range():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT order_date
                    FROM `order` 
                    ORDER BY order_date """
        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def getCategorie():
        conn = DBConnect.get_connection()

        results = dict()

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT *
                        FROM category  """
        cursor.execute(query)

        for row in cursor:
            results[row["id"]] = row["category_name"]



        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getProdotti(cat):
        conn = DBConnect.get_connection()

        results = dict()

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT *
                    FROM product
                    WHERE category_id = %s"""
        cursor.execute(query, (cat,))

        for row in cursor:
            prodotto = Prodotto(id= row['id'],
                                name = row['product_name'],
                                category_id= row['category_id'],
                                list_price= row['list_price'],
                                num_vendite= 0,
                                score= 0)
            results[prodotto.id]= prodotto

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getVendite(dat1, dat2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query =""" SELECT * FROM `order` o
            JOIN order_item oi ON o.id = oi.order_id
            """

        cursor.execute(query)

        for row in cursor:
            if row['shipped_date'] is not None:
                if dat1 <= row['shipped_date'] <= dat2:
                    vendita = Vendita(id=row['id'],
                                      order_id=row['order_id'],
                                      product_id=row['product_id'],
                                      quantity=row['product_id'],
                                      list_price=row['list_price'],
                                      discount= row['discount'],
                                      date=row['shipped_date'])
                    results.append(vendita)

        cursor.close()
        conn.close()
        return results