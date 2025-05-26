import unittest
import os
import sys
import sqlite3

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

class TestMagazine(unittest.TestCase):
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
    
    
    def test_magazine_creation(self):
        """Test creating a magazine"""
        magazine = Magazine("Tech Weekly", "Technology")
        self.assertEqual(magazine.name, "Tech Weekly")
        self.assertEqual(magazine.category, "Technology")
        self.assertIsNone(magazine.id)
    
    def test_magazine_validation(self):
        """Test magazine validation"""
        with self.assertRaises(ValueError):
            Magazine("", "Technology")
        
        with self.assertRaises(ValueError):
            Magazine("Tech Weekly", "")
        
        with self.assertRaises(ValueError):
            Magazine(123, "Technology")
    
    def test_magazine_save(self):
        """Test saving a magazine to database"""
        magazine = Magazine("Tech Weekly", "Technology")
        saved_magazine = magazine.save()
        
        self.assertIsNotNone(saved_magazine.id)
        self.assertEqual(saved_magazine.name, "Tech Weekly")
        self.assertEqual(saved_magazine.category, "Technology")
    
    def test_magazine_find_by_id(self):
        """Test finding magazine by ID"""
        magazine = Magazine("Tech Weekly", "Technology").save()
        found_magazine = Magazine.find_by_id(magazine.id)
        
        self.assertIsNotNone(found_magazine)
        self.assertEqual(found_magazine.name, "Tech Weekly")
        self.assertEqual(found_magazine.category, "Technology")
        self.assertEqual(found_magazine.id, magazine.id)
    
    def test_magazine_find_by_name(self):
        """Test finding magazine by name"""
        magazine = Magazine("Tech Weekly", "Technology").save()
        found_magazine = Magazine.find_by_name("Tech Weekly")
        
        self.assertIsNotNone(found_magazine)
        self.assertEqual(found_magazine.name, "Tech Weekly")
        self.assertEqual(found_magazine.id, magazine.id)
    
    def test_magazine_find_by_category(self):
        """Test finding magazines by category"""
        Magazine("Tech Weekly", "Technology").save()
        Magazine("AI Today", "Technology").save()
        Magazine("Health Tips", "Health").save()
        
        tech_magazines = Magazine.find_by_category("Technology")
        self.assertEqual(len(tech_magazines), 2)
        
        health_magazines = Magazine.find_by_category("Health")
        self.assertEqual(len(health_magazines), 1)
    
    def test_magazine_all(self):
        """Test getting all magazines"""
        Magazine("Tech Weekly", "Technology").save()
        Magazine("Health Tips", "Health").save()
        
        all_magazines = Magazine.all()
        self.assertEqual(len(all_magazines), 2)
    
    def test_magazine_articles(self):
        """Test getting articles in magazine"""
        author = Author("John Doe").save()
        magazine = Magazine("Tech Weekly", "Technology").save()
        
        Article("Article 1", author.id, magazine.id).save()
        Article("Article 2", author.id, magazine.id).save()
        
        articles = magazine.articles()
        self.assertEqual(len(articles), 2)
    
    def test_magazine_contributors(self):
        """Test getting unique contributors to magazine"""
        author1 = Author("John Doe").save()
        author2 = Author("Jane Smith").save()
        magazine = Magazine("Tech Weekly", "Technology").save()
        
        Article("Article 1", author1.id, magazine.id).save()
        Article("Article 2", author2.id, magazine.id).save()
        Article("Article 3", author1.id, magazine.id).save()
        
        contributors = magazine.contributors()
        self.assertEqual(len(contributors), 2)
    
    def test_magazine_article_titles(self):
        """Test getting article titles in magazine"""
        author = Author("John Doe").save()
        magazine = Magazine("Tech Weekly", "Technology").save()
        
        Article("First Article", author.id, magazine.id).save()
        Article("Second Article", author.id, magazine.id).save()
        
        titles = magazine.article_titles()
        self.assertEqual(len(titles), 2)
        self.assertIn("First Article", titles)
        self.assertIn("Second Article", titles)
    
    def test_magazine_contributing_authors(self):
        """Test getting authors with more than 2 articles"""
        author1 = Author("John Doe").save()
        author2 = Author("Jane Smith").save()
        magazine = Magazine("Tech Weekly", "Technology").save()
        
        # Author1 has 3 articles (more than 2)
        Article("Article 1", author1.id, magazine.id).save()
        Article("Article 2", author1.id, magazine.id).save()
        Article("Article 3", author1.id, magazine.id).save()
        
        # Author2 has 1 article (not more than 2)
        Article("Article 4", author2.id, magazine.id).save()
        
        contributing_authors = magazine.contributing_authors()
        self.assertEqual(len(contributing_authors), 1)
    
    def test_magazine_top_publisher(self):
        """Test finding magazine with most articles"""
        author = Author("John Doe").save()
        magazine1 = Magazine("Tech Weekly", "Technology").save()
        magazine2 = Magazine("Science Today", "Science").save()
        
        # Magazine1 has 3 articles
        Article("Article 1", author.id, magazine1.id).save()
        Article("Article 2", author.id, magazine1.id).save()
        Article("Article 3", author.id, magazine1.id).save()
        
        # Magazine2 has 1 article
        Article("Article 4", author.id, magazine2.id).save()
        
        top_publisher = Magazine.top_publisher()
        self.assertIsNotNone(top_publisher)
        self.assertEqual(top_publisher.name, "Tech Weekly")

if __name__ == '__main__':
    unittest.main()