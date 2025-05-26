#!/usr/bin/env python3

import os
import sys

# Add the lib directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection

def run_example_queries():
    """Run example queries to demonstrate the system"""
    
    print("=" * 60)
    print("Articles Management System - Example Queries")
    print("=" * 60)
    
    try:
        # Basic data retrieval
        print("\n1. All Authors:")
        authors = Author.all()
        for author in authors:
            print(f"   - {author.name} (ID: {author.id})")
        
        print("\n2. All Magazines:")
        magazines = Magazine.all()
        for magazine in magazines:
            print(f"   - {magazine.name} ({magazine.category}) (ID: {magazine.id})")
        
        print("\n3. All Articles:")
        articles = Article.all()
        for article in articles:
            print(f"   - {article.title} (Author ID: {article.author_id}, Magazine ID: {article.magazine_id})")
        
        # Relationship queries
        if authors:
            sample_author = authors[0]
            print(f"\n4. Articles by {sample_author.name}:")
            author_articles = sample_author.articles()
            for article in author_articles:
                print(f"   - {article['title']}")
            
            print(f"\n5. Magazines {sample_author.name} has written for:")
            author_magazines = sample_author.magazines()
            for magazine in author_magazines:
                print(f"   - {magazine['name']} ({magazine['category']})")
            
            print(f"\n6. Topic areas {sample_author.name} has written about:")
            topic_areas = sample_author.topic_areas()
            for topic in topic_areas:
                print(f"   - {topic}")
        
        if magazines:
            sample_magazine = magazines[0]
            print(f"\n7. Articles in {sample_magazine.name}:")
            magazine_articles = sample_magazine.articles()
            for article in magazine_articles:
                print(f"   - {article['title']}")
            
            print(f"\n8. Contributors to {sample_magazine.name}:")
            contributors = sample_magazine.contributors()
            for contributor in contributors:
                print(f"   - {contributor['name']}")
            
            print(f"\n9. Article titles in {sample_magazine.name}:")
            titles = sample_magazine.article_titles()
            for title in titles:
                print(f"   - {title}")
            
            print(f"\n10. Contributing authors (>2 articles) in {sample_magazine.name}:")
            contributing_authors = sample_magazine.contributing_authors()
            if contributing_authors:
                for author in contributing_authors:
                    print(f"    - {author['name']}")
            else:
                print("    - No authors with more than 2 articles")
        
        # Advanced queries
        print("\n11. Top Publisher (magazine with most articles):")
        top_publisher = Magazine.top_publisher()
        if top_publisher:
            print(f"    - {top_publisher.name} ({top_publisher.category})")
        else:
            print("    - No articles published yet")
        
        # Custom SQL queries
        print("\n12. Custom SQL Queries:")
        
        print("\n    a) Magazines with articles by at least 2 different authors:")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.name, m.category, COUNT(DISTINCT art.author_id) as author_count
            FROM magazines m
            JOIN articles art ON m.id = art.magazine_id
            GROUP BY m.id
            HAVING author_count >= 2
        """)
        results = cursor.fetchall()
        for row in results:
            print(f"       - {row['name']} ({row['category']}) - {row['author_count']} authors")
        
        print("\n    b) Count of articles in each magazine:")
        cursor.execute("""
            SELECT m.name, COUNT(art.id) as article_count
            FROM magazines m
            LEFT JOIN articles art ON m.id = art.magazine_id
            GROUP BY m.id
            ORDER BY article_count DESC
        """)
        results = cursor.fetchall()
        for row in results:
            print(f"       - {row['name']}: {row['article_count']} articles")
        
        print("\n    c) Author who has written the most articles:")
        cursor.execute("""
            SELECT a.name, COUNT(art.id) as article_count
            FROM authors a
            LEFT JOIN articles art ON a.id = art.author_id
            GROUP BY a.id
            ORDER BY article_count DESC
            LIMIT 1
        """)
        result = cursor.fetchone()
        if result:
            print(f"       - {result['name']}: {result['article_count']} articles")
        
        conn.close()
        
    except Exception as e:
        print(f"Error running queries: {e}")
        print("Make sure to run 'python scripts/setup_db.py' and 'python lib/db/seed.py' first")
    
    print("\n" + "=" * 60)
    print("Query examples completed!")
    print("=" * 60)

if __name__ == "__main__":
    run_example_queries()