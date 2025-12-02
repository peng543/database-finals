# db/connection.py
import os
import logging
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import pooling, Error

load_dotenv()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

POOL = None

def init_pool(pool_name="student_pool", pool_size=None):
    """
    Initialize a connection pool. Safe to call multiple times.
    pool_size can be provided via environment variable POOL_SIZE.
    """
    global POOL
    if POOL is not None:
        return

    pool_size = pool_size or int(os.getenv("POOL_SIZE", 5))
    conn_kwargs = dict(
        pool_name=pool_name,
        pool_size=pool_size,
        pool_reset_session=True,
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "")
    )

    db_name = os.getenv("DB_NAME", "").strip()
    if db_name:
        conn_kwargs["database"] = db_name

    # Log if using default credentials (likely missing .env)
    if os.getenv("DB_USER") is None:
        logger.warning("DB_USER not set; using default 'root'. Check .env file.")
    if os.getenv("DB_PASSWORD") is None:
        logger.warning("DB_PASSWORD not set; using empty password. Check .env file.")

    try:
        POOL = pooling.MySQLConnectionPool(**conn_kwargs)
        logger.info("MySQL connection pool created (size=%s, host=%s)", pool_size, conn_kwargs['host'])
    except Error as e:
        logger.exception("Failed to initialize MySQL pool: %s", e)
        raise

def get_connection():
    """Return a pooled connection. Ensure init_pool() is called during app startup."""
    global POOL
    if POOL is None:
        init_pool()
    return POOL.get_connection()

def test_connection():
    """
    Try to get a connection and run a simple query.
    Returns (True, None) on success, (False, error_string) on failure.
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.fetchall()
        cur.close()
        conn.close()
        return True, None
    except Exception as e:
        return False, str(e)


