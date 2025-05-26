import unittest
import os
import sys
import sqlite3

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection

class TestAuthor(unittest.TestCase):
    def setUp(self):
        """Set up test database"""
        # Set testing environment variable
        os.environ['TESTING'] = '1'
        
        # Create tables
        conn = get_connection()
        conn.execute('''CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )''')
        conn.execute('''CREATE TABLE IF NOT EXISTS magazines (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            category VARCHAR(255) NOT NULL
        )''')
        conn.execute('''CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author_id INTEGER,
            magazine_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES authors(id),
            FOREIGN KEY (magazine_id) REFERENCES magazines(id)
        )''')
        conn.commit()
        conn.close()
    
    def tearDown(self):
        """Clean up test database"""
        # Clear tables
        conn = get_connection()
        conn.execute('DELETE FROM articles')
        conn.execute('DELETE FROM authors')
        conn.execute('DELETE FROM magazines')
        conn.commit()
        conn.close()
        
        # Remove testing environment variable
        if 'TESTING' in os.environ:
            del os.environ['TESTING']
        
        # Remove test database file
        if os.path.exists('test_articles.db'):
            os.remove('test_articles.db')
    
    
    def test_author_creation(self):
        """Test creating an author"""
        author = Author("John Doe")
        self.assertEqual(author.name, "John Doe")
        self.assertIsNone(author.id)
    
    def test_author_name_validation(self):
        """Test author name validation"""
        with self.assertRaises(ValueError):
            Author("")
        
        with self.assertRaises(ValueError):
            Author(123)
    
    def test_author_save(self):
        """Test saving an author to database"""
        author = Author("John Doe")
        saved_author = author.save()
        
        self.assertIsNotNone(saved_author.id)
        self.assertEqual(saved_author.name, "John Doe")
    
    def test_author_find_by_id(self):
        """Test finding author by ID"""
        author = Author("John Doe").save()
        found_author = Author.find_by_id(author.id)
        
        self.assertIsNotNone(found_author)
        self.assertEqual(found_author.name, "John Doe")
        self.assertEqual(found_author.id, author.id)
    
    def test_author_find_by_name(self):
        """Test finding author by name"""
        author = Author("John Doe").save()
        found_author = Author.find_by_name("John Doe")
        
        self.assertIsNotNone(found_author)
        self.assertEqual(found_author.name, "John Doe")
        self.assertEqual(found_author.id, author.id)
    
    def test_author_all(self):
        """Test getting all authors"""
        Author("John Doe").save()
        Author("Jane Smith").save()
        
        all_authors = Author.all()
        self.assertEqual(len(all_authors), 2)
        
        names = [author.name for author in all_authors]
        self.assertIn("John Doe", names)
        self.assertIn("Jane Smith", names)
    
    def test_author_articles(self):
        """Test getting articles by author"""
        author = Author("John Doe").save()
        magazine = Magazine("Tech Weekly", "Technology").save()
        
        Article("Article 1", author.id, magazine.id).save()
        Article("Article 2", author.id, magazine.id).save()
        
        articles = author.articles()
        self.assertEqual(len(articles), 2)
    
    def test_author_magazines(self):
        """Test getting magazines author has written for"""
        author = Author("John Doe").save()
        magazine1 = Magazine("Tech Weekly", "Technology").save()
        magazine2 = Magazine("Science Today", "Science").save()
        
        Article("Article 1", author.id, magazine1.id).save()
        Article("Article 2", author.id, magazine2.id).save()
        
        magazines = author.magazines()
        self.assertEqual(len(magazines), 2)
    
    def test_author_add_article(self):
        """Test adding article through author"""
        author = Author("John Doe").save()
        magazine = Magazine("Tech Weekly", "Technology").save()
        
        article = author.add_article(magazine, "New Article")
        self.assertIsNotNone(article.id)
        self.assertEqual(article.title, "New Article")
        self.assertEqual(article.author_id, author.id)
        self.assertEqual(article.magazine_id, magazine.id)
    
    def test_author_topic_areas(self):
        """Test getting topic areas (categories) author has written for"""
        author = Author("John Doe").save()
        magazine1 = Magazine("Tech Weekly", "Technology").save()
        magazine2 = Magazine("Science Today", "Science").save()
        
        Article("Article 1", author.id, magazine1.id).save()
        Article("Article 2", author.id, magazine2.id).save()
        
        topic_areas = author.topic_areas()
        self.assertEqual(len(topic_areas), 2)
        self.assertIn("Technology", topic_areas)
        self.assertIn("Science", topic_areas)

if __name__ == '__main__':
    unittest.main()