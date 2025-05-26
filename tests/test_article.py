import unittest
import os
import sys
import sqlite3

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

class TestArticle(unittest.TestCase):
    def setUp(self):
        """Set up test database"""
        # Set testing environment variable
        os.environ['TESTING'] = '1'
        
        # Create tables
        from lib.db.connection import get_connection
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
        from lib.db.connection import get_connection
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
    
    
    def test_article_creation(self):
        """Test creating an article"""
        article = Article("Test Title", 1, 1)
        self.assertEqual(article.title, "Test Title")
        self.assertEqual(article.author_id, 1)
        self.assertEqual(article.magazine_id, 1)
        self.assertIsNone(article.id)
    
    def test_article_title_validation(self):
        """Test article title validation"""
        with self.assertRaises(ValueError):
            Article("", 1, 1)
        
        with self.assertRaises(ValueError):
            Article(123, 1, 1)
    
    def test_article_save(self):
        """Test saving an article to database"""
        # First create author and magazine
        author = Author("John Doe").save()
        magazine = Magazine("Tech Weekly", "Technology").save()
        
        article = Article("Test Article", author.id, magazine.id)
        saved_article = article.save()
        
        self.assertIsNotNone(saved_article.id)
        self.assertEqual(saved_article.title, "Test Article")
        self.assertEqual(saved_article.author_id, author.id)
        self.assertEqual(saved_article.magazine_id, magazine.id)
    
    def test_article_find_by_id(self):
        """Test finding article by ID"""
        author = Author("John Doe").save()
        magazine = Magazine("Tech Weekly", "Technology").save()
        article = Article("Test Article", author.id, magazine.id).save()
        
        found_article = Article.find_by_id(article.id)
        
        self.assertIsNotNone(found_article)
        self.assertEqual(found_article.title, "Test Article")
        self.assertEqual(found_article.id, article.id)
    
    def test_article_find_by_title(self):
        """Test finding articles by title"""
        author = Author("John Doe").save()
        magazine = Magazine("Tech Weekly", "Technology").save()
        
        Article("Test Article", author.id, magazine.id).save()
        Article("Test Article", author.id, magazine.id).save()  # Same title
        Article("Different Title", author.id, magazine.id).save()
        
        found_articles = Article.find_by_title("Test Article")
        self.assertEqual(len(found_articles), 2)
    
    def test_article_find_by_author(self):
        """Test finding articles by author"""
        author1 = Author("John Doe").save()
        author2 = Author("Jane Smith").save()
        magazine = Magazine("Tech Weekly", "Technology").save()
        
        Article("Article 1", author1.id, magazine.id).save()
        Article("Article 2", author1.id, magazine.id).save()
        Article("Article 3", author2.id, magazine.id).save()
        
        author1_articles = Article.find_by_author(author1.id)
        self.assertEqual(len(author1_articles), 2)
        
        author2_articles = Article.find_by_author(author2.id)
        self.assertEqual(len(author2_articles), 1)
    
    def test_article_find_by_magazine(self):
        """Test finding articles by magazine"""
        author = Author("John Doe").save()
        magazine1 = Magazine("Tech Weekly", "Technology").save()
        magazine2 = Magazine("Science Today", "Science").save()
        
        Article("Article 1", author.id, magazine1.id).save()
        Article("Article 2", author.id, magazine1.id).save()
        Article("Article 3", author.id, magazine2.id).save()
        
        magazine1_articles = Article.find_by_magazine(magazine1.id)
        self.assertEqual(len(magazine1_articles), 2)
        
        magazine2_articles = Article.find_by_magazine(magazine2.id)
        self.assertEqual(len(magazine2_articles), 1)
    
    def test_article_all(self):
        """Test getting all articles"""
        author = Author("John Doe").save()
        magazine = Magazine("Tech Weekly", "Technology").save()
        
        Article("Article 1", author.id, magazine.id).save()
        Article("Article 2", author.id, magazine.id).save()
        
        all_articles = Article.all()
        self.assertEqual(len(all_articles), 2)
    
    def test_article_author_relationship(self):
        """Test getting author from article"""
        author = Author("John Doe").save()
        magazine = Magazine("Tech Weekly", "Technology").save()
        article = Article("Test Article", author.id, magazine.id).save()
        
        article_author = article.author()
        self.assertIsNotNone(article_author)
        self.assertEqual(article_author.name, "John Doe")
        self.assertEqual(article_author.id, author.id)
    
    def test_article_magazine_relationship(self):
        """Test getting magazine from article"""
        author = Author("John Doe").save()
        magazine = Magazine("Tech Weekly", "Technology").save()
        article = Article("Test Article", author.id, magazine.id).save()
        
        article_magazine = article.magazine()
        self.assertIsNotNone(article_magazine)
        self.assertEqual(article_magazine.name, "Tech Weekly")
        self.assertEqual(article_magazine.id, magazine.id)

if __name__ == '__main__':
    unittest.main()