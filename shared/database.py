import psycopg2
from shared.config import settings

_connection = None

def get_db_connection() -> object:
    """
    Establishes and returns a connection to the PostgreSQL database using psycopg2.

    Returns:
        object: A connection object to the PostgreSQL database.
    """

    global _connection
    if _connection is None:
        try:
            _connection = psycopg2.connect(settings.DATABASE_URL)
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            
    return _connection

def save_vector(tenant_id: str, document_id: str, chunk_text: str, embedding: list[float]) -> None:
    """
    Saves a vector embedding to the PostgreSQL database.

    Args:
        tenant_id (str): The ID of the tenant.
        document_id (str): The ID of the document.
        chunk_text (str): The text of the chunk.
        embedding (list[float]): The vector embedding.

    Returns:
        None
    """
    insert_query = """
        INSERT INTO documents(tenant_id, document_id, chunk_text, embedding)
        VALUES (%s,%s,%s,%s)
    """
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(insert_query,(tenant_id,document_id,chunk_text,embedding))

        conn.commit()
        print("Data inserted into superbase")

    except Exception as e:
        # Rollback changes if anything goes wrong during the execution
        if conn:
            conn.rollback()
        print(f"Failed to insert data: {e}")
        
