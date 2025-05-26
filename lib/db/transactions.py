from lib.db.connection import get_connection

def add_author_with_articles(author_name, articles_data):
    """
    Add an author and their articles in a single transaction
    articles_data: list of dicts with 'title' and 'magazine_id' keys
    """
    conn = get_connection()
    try:
        conn.execute("BEGIN TRANSACTION")
        cursor = conn.cursor()
        
        # Insert author
        cursor.execute(
            "INSERT INTO authors (name) VALUES (?)",
            (author_name,)
        )
        author_id = cursor.lastrowid
        
        # Insert articles
        for article in articles_data:
            cursor.execute(
                "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                (article['title'], author_id, article['magazine_id'])
            )
        
        conn.execute("COMMIT")
        print(f"Successfully added author '{author_name}' with {len(articles_data)} articles")
        return True
    except Exception as e:
        conn.execute("ROLLBACK")
        print(f"Transaction failed: {e}")
        return False
    finally:
        conn.close()

def transfer_articles_between_magazines(from_magazine_id, to_magazine_id, article_ids):
    """
    Transfer multiple articles from one magazine to another in a single transaction
    """
    conn = get_connection()
    try:
        conn.execute("BEGIN TRANSACTION")
        cursor = conn.cursor()
        
        # Update all specified articles
        for article_id in article_ids:
            cursor.execute(
                "UPDATE articles SET magazine_id = ? WHERE id = ? AND magazine_id = ?",
                (to_magazine_id, article_id, from_magazine_id)
            )
            
            # Check if the article was actually updated
            if cursor.rowcount == 0:
                raise Exception(f"Article {article_id} not found in source magazine or doesn't exist")
        
        conn.execute("COMMIT")
        print(f"Successfully transferred {len(article_ids)} articles between magazines")
        return True
    except Exception as e:
        conn.execute("ROLLBACK")
        print(f"Transaction failed: {e}")
        return False
    finally:
        conn.close()

def delete_author_and_articles(author_id):
    """
    Delete an author and all their articles in a single transaction
    """
    conn = get_connection()
    try:
        conn.execute("BEGIN TRANSACTION")
        cursor = conn.cursor()
        
        # First delete all articles by this author
        cursor.execute("DELETE FROM articles WHERE author_id = ?", (author_id,))
        articles_deleted = cursor.rowcount
        
        # Then delete the author
        cursor.execute("DELETE FROM authors WHERE id = ?", (author_id,))
        author_deleted = cursor.rowcount
        
        if author_deleted == 0:
            raise Exception(f"Author with ID {author_id} not found")
        
        conn.execute("COMMIT")
        print(f"Successfully deleted author and {articles_deleted} articles")
        return True
    except Exception as e:
        conn.execute("ROLLBACK")
        print(f"Transaction failed: {e}")
        return False
    finally:
        conn.close()