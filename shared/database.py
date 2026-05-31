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
    cursor = None
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
    
    finally:
        if cursor:
            cursor.close()
        
def fetch_isolated_context (query_vector: list[float], tenant_id: str, limit: int = 4) -> list[dict]:
    """
    Fetches the most relevant context chunks from the database based on cosine similarity to the query vector.

    Args:
        query_vector (list[float]): The vector embedding of the user's query.
        tenant_id (str): The ID of the tenant to filter the documents.
        limit (int, optional): The maximum number of context chunks to return. Defaults to 4
    
    Returns:
        list[dict]: A list of dictionaries containing the chunk text, document ID, and similarity score for the most relevant context chunks.
    """
    
    fetch_query = """
        SELECT chunk_text, document_id, 1 - (embedding <=> %s::vector) AS similarity
        FROM documents
        WHERE tenant_id = %s
        ORDER BY embedding <=> %s::vector
        LIMIT %s
    """
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(fetch_query,(query_vector,tenant_id,query_vector,limit))

        rows = cursor.fetchall()
        
        return [{"chunk_text":row[0],"document_id":row[1],"similarity":row[2]} for row in rows] # the cursor.fetchall() returns list of tuples so we use lisat comprehension for fetching dataa

    except Exception as e:
        return []

    finally:
        if cursor:
            cursor.close()