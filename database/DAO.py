from database.DB_connect import DBConnect
from model.archi import Arco
from model.card import Card
class DAO():
    def __init__(self):
        return

    def getAllNodes(min,max,limite):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """WITH sample_battles AS (
                        SELECT * FROM battles_named 
                        WHERE (p1trophies BETWEEN %s AND %s OR p2trophies BETWEEN %s AND %s)
                        LIMIT %s
                    )
                    SELECT card_name, COUNT(*) AS quantita 
                    FROM (
                        
                        SELECT p1_card1 AS card_name FROM sample_battles WHERE p1trophies BETWEEN %s AND %s
                        UNION ALL SELECT p1_card2 FROM sample_battles WHERE p1trophies BETWEEN %s AND %s
                        UNION ALL SELECT p1_card3 FROM sample_battles WHERE p1trophies BETWEEN %s AND %s
                        UNION ALL SELECT p1_card4 FROM sample_battles WHERE p1trophies BETWEEN %s AND %s
                        UNION ALL SELECT p1_card5 FROM sample_battles WHERE p1trophies BETWEEN %s AND %s
                        UNION ALL SELECT p1_card6 FROM sample_battles WHERE p1trophies BETWEEN %s AND %s
                        UNION ALL SELECT p1_card7 FROM sample_battles WHERE p1trophies BETWEEN %s AND %s
                        UNION ALL SELECT p1_card8 FROM sample_battles WHERE p1trophies BETWEEN %s AND %s
                        UNION ALL
                        
                        SELECT p2_card1 AS card_name FROM sample_battles WHERE p2trophies BETWEEN %s AND %s
                        UNION ALL SELECT p2_card2 FROM sample_battles WHERE p2trophies BETWEEN %s AND %s
                        UNION ALL SELECT p2_card3 FROM sample_battles WHERE p2trophies BETWEEN %s AND %s
                        UNION ALL SELECT p2_card4 FROM sample_battles WHERE p2trophies BETWEEN %s AND %s
                        UNION ALL SELECT p2_card5 FROM sample_battles WHERE p2trophies BETWEEN %s AND %s
                        UNION ALL SELECT p2_card6 FROM sample_battles WHERE p2trophies BETWEEN %s AND %s
                        UNION ALL SELECT p2_card7 FROM sample_battles WHERE p2trophies BETWEEN %s AND %s
                        UNION ALL SELECT p2_card8 FROM sample_battles WHERE p2trophies BETWEEN %s AND %s
                    ) AS all_cards
                    WHERE card_name IS NOT NULL
                    GROUP BY card_name
                    ORDER BY quantita DESC;"""

        cursor.execute(query,(min,max,min,max,limite,min,max,min,max,min,max,min,max,min,max,min,max,min,max,min,max,min,max,min,max,min,max,min,max,min,max,min,max,min,max,min,max,))
        for row in cursor:
            result.append(Card(**row))

        cursor.close()
        conn.close()
        return result

    def getAllEdges(min,max,limite):
        conn=DBConnect.get_connection()
        cursor=conn.cursor(dictionary=True)
        result=[]
        query="""SELECT card_a, card_b, SUM(quantita) AS peso
                    FROM (
                        
                        WITH campione AS (
                            SELECT * FROM battles_named 
                            WHERE p1trophies BETWEEN %s AND %s 
                               OR p2trophies BETWEEN %s AND %s
                            LIMIT %s
                        )
                        
                        SELECT p1_card1 AS card_a, p1_card2 AS card_b, COUNT(*) AS quantita FROM campione GROUP BY 1,2
                        UNION ALL SELECT p1_card1, p1_card3, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p1_card1, p1_card4, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p1_card1, p1_card5, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p1_card1, p1_card6, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p1_card1, p1_card7, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p1_card1, p1_card8, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p1_card2, p1_card3, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p1_card2, p1_card4, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p1_card2, p1_card5, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p1_card2, p1_card6, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p1_card2, p1_card7, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p1_card2, p1_card8, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p1_card3, p1_card4, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p1_card3, p1_card5, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p1_card3, p1_card6, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p1_card3, p1_card7, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p1_card3, p1_card8, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p1_card4, p1_card5, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p1_card4, p1_card6, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p1_card4, p1_card7, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p1_card4, p1_card8, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p1_card5, p1_card6, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p1_card5, p1_card7, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p1_card5, p1_card8, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p1_card6, p1_card7, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p1_card6, p1_card8, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p1_card7, p1_card8, COUNT(*) FROM campione GROUP BY 1,2
                        
                        UNION ALL
                        
                        SELECT p2_card1, p2_card2, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p2_card1, p2_card3, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p2_card1, p2_card4, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p2_card1, p2_card5, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p2_card1, p2_card6, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p2_card1, p2_card7, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p2_card1, p2_card8, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p2_card2, p2_card3, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p2_card2, p2_card4, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p2_card2, p2_card5, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p2_card2, p2_card6, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p2_card2, p2_card7, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p2_card2, p2_card8, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p2_card3, p2_card4, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p2_card3, p2_card5, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p2_card3, p2_card6, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p2_card3, p2_card7, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p2_card3, p2_card8, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p2_card4, p2_card5, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p2_card4, p2_card6, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p2_card4, p2_card7, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p2_card4, p2_card8, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p2_card5, p2_card6, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p2_card5, p2_card7, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p2_card5, p2_card8, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p2_card6, p2_card7, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p2_card6, p2_card8, COUNT(*) FROM campione GROUP BY 1,2
                        UNION ALL SELECT p2_card7, p2_card8, COUNT(*) FROM campione GROUP BY 1,2
                    ) AS all_pairs
                    WHERE card_a IS NOT NULL AND card_b IS NOT NULL
                    GROUP BY card_a, card_b
                    ORDER BY peso DESC;"""
        cursor.execute(query,(min,max,min,max,limite,))
        for row in cursor:
            result.append(Arco(**row))

        cursor.close()
        conn.close()
        return result


