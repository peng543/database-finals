# db/queries.py
import pandas as pd
from .connection import get_connection

def read_view(view_name, limit=None):
    conn = get_connection()
    sql = f"SELECT * FROM {view_name}"
    if limit:
        sql += " LIMIT %s"
        df = pd.read_sql(sql, conn, params=(limit,))
    else:
        df = pd.read_sql(sql, conn)
    conn.close()
    return df

def call_sp_register_course(student_id, course_id, semester, academic_year):
    conn = get_connection()
    cur = conn.cursor()
    # Using CALL ensures any SELECT inside the SP returns results to client
    cur.execute("CALL sp_register_course(%s,%s,%s,%s)",
                (student_id, course_id, semester, academic_year), multi = True)
    # fetch all result sets produced by the procedure
    results = []
    try:
        while True:
            res = cur.fetchall()
            results.append(res)
            if not cur.nextset():
                break
    except Exception:
        # if no rows returned, ignore
        pass
    cur.close()
    conn.commit()
    conn.close()
    return results

def call_sp_semester_revenue_report(year, semester):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL sp_semester_revenue_report(%s,%s)", (year, semester), multi = True)
    cols = [d[0] for d in cur.description] if cur.description else []
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return pd.DataFrame(rows, columns=cols) if cols else pd.DataFrame(rows)
