from django.db import connection

def execute_query(query, params=None, fetchone=False, fetchall=False):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        if fetchone:
            row = cursor.fetchone()
            columns = [col[0] for col in cursor.description]
            return dict(zip(columns, row)) if row else None 
        if fetchall:
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        connection.commit()

