# db/crud.py
import pandas as pd
from .connection import get_connection
from mysql.connector import Error

# ---- STUDENTS ----
def create_student(full_name,
                   date_of_birth,
                   gender,
                   email,
                   phone_number=None,
                   address=None,
                   program_id=None,
                   enrollment_year=None,
                   student_id=None):
    """
    If student_id is provided, include it in the insert (works with non AUTO_INCREMENT schema).
    If not provided, omit it (works with AUTO_INCREMENT).
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        if student_id is not None:
            sql = ("INSERT INTO STUDENT "
                   "(student_id, full_name, date_of_birth, gender, email, phone_number, address, program_id, enrollment_year) "
                   "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            params = (student_id, full_name, date_of_birth, gender, email, phone_number, address, program_id, enrollment_year)
        else:
            sql = ("INSERT INTO STUDENT "
                   "(full_name, date_of_birth, gender, email, phone_number, address, program_id, enrollment_year) "
                   "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)")
            params = (full_name, date_of_birth, gender, email, phone_number, address, program_id, enrollment_year)
        cur.execute(sql, params)
        conn.commit()
        last_id = cur.lastrowid
        cur.close()
        conn.close()
        return True, last_id
    except Error as e:
        return False, str(e)

def read_students(limit=1000):
    try:
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM STUDENT LIMIT %s", conn, params=(limit,))
        conn.close()
        return df, None
    except Exception as e:
        return None, str(e)

def update_student(student_id,
                   full_name,
                   date_of_birth,
                   gender,
                   email,
                   phone_number=None,
                   address=None,
                   program_id=None,
                   enrollment_year=None):
    try:
        conn = get_connection()
        cur = conn.cursor()
        sql = ("UPDATE STUDENT SET full_name=%s, date_of_birth=%s, gender=%s, email=%s, "
               "phone_number=%s, address=%s, program_id=%s, enrollment_year=%s WHERE student_id=%s")
        cur.execute(sql, (full_name, date_of_birth, gender, email, phone_number, address, program_id, enrollment_year, student_id))
        conn.commit()
        cur.close()
        conn.close()
        return True, None
    except Error as e:
        return False, str(e)

def delete_student(student_id):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM STUDENT WHERE student_id=%s", (student_id,))
        conn.commit()
        cur.close()
        conn.close()
        return True, None
    except Error as e:
        return False, str(e)

# ---- TUITION & PAYMENTS ----
def read_tuition_by_feeid(fee_id):
    """Read a single tuition fee record by fee_id."""
    try:
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM TUITION_FEE WHERE fee_id=%s", conn, params=(fee_id,))
        conn.close()
        return df
    except Exception as e:
        return pd.DataFrame()

def insert_payment(fee_id, amount):
    """Record a payment for a tuition fee. Updates amount_paid."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        # Get current amount_paid
        cur.execute("SELECT amount_paid FROM TUITION_FEE WHERE fee_id=%s", (fee_id,))
        row = cur.fetchone()
        if not row:
            return False, "Fee ID not found"
        current_paid = row[0] or 0 
        new_paid = float(current_paid) + amount
        # Update amount_paid
        cur.execute("UPDATE TUITION_FEE SET amount_paid=%s WHERE fee_id=%s", (new_paid, fee_id))
        conn.commit()
        cur.close()
        conn.close()
        return True, None
    except Error as e:
        return False, str(e)

# ---- ENROLLMENTS ----
def read_enrollments(student_id=None, limit=1000):
    """Read enrollments, optionally filtered by student_id."""
    try:
        conn = get_connection()
        if student_id:
            df = pd.read_sql(
                """SELECT e.enrollment_id, e.student_id, s.full_name, e.course_id, c.course_name,
                          e.semester, e.academic_year, e.grade, e.status 
                   FROM ENROLLMENT e 
                   LEFT JOIN STUDENT s ON e.student_id = s.student_id
                   LEFT JOIN COURSE c ON e.course_id = c.course_id
                   WHERE e.student_id=%s 
                   LIMIT %s""",
                conn, params=(student_id, limit)
            )
        else:
            df = pd.read_sql(
                """SELECT e.enrollment_id, e.student_id, s.full_name, e.course_id, c.course_name,
                          e.semester, e.academic_year, e.grade, e.status 
                   FROM ENROLLMENT e 
                   LEFT JOIN STUDENT s ON e.student_id = s.student_id
                   LEFT JOIN COURSE c ON e.course_id = c.course_id
                   LIMIT %s""",
                conn, params=(limit,)
            )
        conn.close()
        return df
    except Exception as e:
        return pd.DataFrame()
