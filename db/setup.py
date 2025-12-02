# db/setup.py
from .connection import get_connection
from mysql.connector import Error

EXPECTED_TABLES = ["PROGRAM", "STUDENT", "INSTRUCTOR", "COURSE", "ENROLLMENT", "TUITION_FEE", "ADVISOR_ASSIGNMENT"]


def table_exists(conn, table_name):
    cur = conn.cursor()
    cur.execute("SHOW TABLES LIKE %s", (table_name,))
    exists = cur.fetchone() is not None
    cur.close()
    return exists

def find_missing_tables():
    """Return list of expected tables that are missing in the current DB."""
    conn = get_connection()
    missing = []
    for t in EXPECTED_TABLES:
        if not table_exists(conn, t):
            missing.append(t)
    conn.close()
    return missing

def create_demo_schema():
    """
    Create a minimal demo schema for development/test when the real schema isn't ready.
    Safe to run multiple times (uses IF NOT EXISTS and idempotent inserts).
    """
    conn = get_connection()
    cur = conn.cursor()
    # Minimal DDL: PROGRAM, STUDENT, COURSE, ENROLLMENT, INSTRUCTOR, TUITION_FEE, ADVISOR_ASSIGNMENT
    ddls = [
        """
        CREATE TABLE IF NOT EXISTS PROGRAM (
            program_id INT PRIMARY KEY AUTO_INCREMENT,
            program_name VARCHAR(100) NOT NULL
        ) ENGINE=InnoDB;
        """,
        """
        CREATE TABLE IF NOT EXISTS STUDENT (
            student_id INT AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(200) NOT NULL,
            date_of_birth DATE,
            gender ENUM('Male','Female','Other') DEFAULT 'Male',
            email VARCHAR(100),
            phone_number VARCHAR(15),
            address TEXT,
            program_id INT,
            enrollment_year INT,
            FOREIGN KEY (program_id) REFERENCES PROGRAM(program_id)
        ) ENGINE=InnoDB;
        """,
        """
        CREATE TABLE IF NOT EXISTS INSTRUCTOR (
            instructor_id INT AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(200) NOT NULL,
            email VARCHAR(100),
            phone_number VARCHAR(15),
            department VARCHAR(100)
        ) ENGINE=InnoDB;
        """,
        """
        CREATE TABLE IF NOT EXISTS COURSE (
            course_id INT AUTO_INCREMENT PRIMARY KEY,
            course_name VARCHAR(200),
            credit_hours INT,
            instructor_id INT,
            FOREIGN KEY (instructor_id) REFERENCES INSTRUCTOR(instructor_id)
        ) ENGINE=InnoDB;
        """,
        """
        CREATE TABLE IF NOT EXISTS ENROLLMENT (
            enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            course_id INT,
            semester VARCHAR(10),
            academic_year INT,
            grade DECIMAL(4,2),
            status VARCHAR(20),
            FOREIGN KEY (student_id) REFERENCES STUDENT(student_id),
            FOREIGN KEY (course_id) REFERENCES COURSE(course_id)
        ) ENGINE=InnoDB;
        """,
        """
        CREATE TABLE IF NOT EXISTS TUITION_FEE (
            fee_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            total_amount DECIMAL(10,2),
            amount_paid DECIMAL(10,2) DEFAULT 0,
            due_date DATE,
            FOREIGN KEY (student_id) REFERENCES STUDENT(student_id)
        ) ENGINE=InnoDB;
        """,
        """
        CREATE TABLE IF NOT EXISTS ADVISOR_ASSIGNMENT (
            assignment_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            advisor_id INT,
            assignment_date DATE,
            FOREIGN KEY (student_id) REFERENCES STUDENT(student_id),
            FOREIGN KEY (advisor_id) REFERENCES INSTRUCTOR(instructor_id)
        ) ENGINE=InnoDB;
        """
    ]
    try:
        for ddl in ddls:
            cur.execute(ddl)
        # Seed a couple of programs and students if not present
        cur.execute("""
            INSERT IGNORE INTO PROGRAM (program_name) 
            VALUES ('Economics'), ('Computer Science')
        """)
        cur.execute("""
            INSERT INTO STUDENT (full_name, date_of_birth, gender, email, program_id, enrollment_year)
            SELECT * FROM (
                SELECT 'Nguyen Van A', '2003-06-10', 'Male', 'nguyenvana@example.com', 1, 2023 UNION ALL
                SELECT 'Tran Thi B', '2002-11-02', 'Female', 'tranthib@example.com', 2, 2023
            ) AS tmp
            WHERE NOT EXISTS (SELECT 1 FROM STUDENT WHERE full_name='Nguyen Van A')
        """)
        cur.execute("""
            INSERT INTO INSTRUCTOR (full_name, email, department)
            SELECT * FROM (
                SELECT 'Dr. Pham Minh C', 'phamc@example.com', 'Economics' UNION ALL
                SELECT 'Prof. Le Thi D', 'letid@example.com', 'Computer Science'
            ) AS tmp
            WHERE NOT EXISTS (SELECT 1 FROM INSTRUCTOR WHERE full_name='Dr. Pham Minh C')
        """)
        conn.commit()
    except Error as e:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()
    return True
