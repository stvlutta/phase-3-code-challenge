#!/usr/bin/env python3

import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.transactions import add_author_with_articles

def main():
    """Interactive debugging session for the articles system"""
    
    print("=" * 50)
    print("Articles Management System - Debug Console")
    print("=" * 50)
    
    # Set up database if needed
    try:
        # Try to create a simple test to see if database exists
        Author.all()
        print("✓ Database connection successful")
    except Exception as e:
        print(f"⚠ Database error: {e}")
        print("Run 'python scripts/setup_db.py' first to set up the database")
        return
    
    # Show current data
    print(f"\nCurrent data:")
    print(f"Authors: {len(Author.all())}")
    print(f"Magazines: {len(Magazine.all())}")
    print(f"Articles: {len(Article.all())}")
    
    print("\n" + "=" * 50)
    print("Available objects for testing:")
    print("=" * 50)
    print("Classes: Author, Magazine, Article")
    print("Functions: add_author_with_articles")
    print("\nExample usage:")
    print("  author = Author('John Doe').save()")
    print("  magazine = Magazine('Tech Weekly', 'Technology').save()")
    print("  article = Article('AI Future', author.id, magazine.id).save()")
    print("  articles = author.articles()")
    print("  magazines = author.magazines()")
    print("\nTransaction example:")
    print("  add_author_with_articles('New Author', [")
    print("      {'title': 'Article 1', 'magazine_id': 1},")
    print("      {'title': 'Article 2', 'magazine_id': 2}")
    print("  ])")
    
    print("\n" + "=" * 50)
    print("Sample data queries:")
    print("=" * 50)
    
    # Show some sample data if it exists
    authors = Author.all()
    if authors:
        print(f"\nSample authors:")
        for author in authors[:3]:
            print(f"  - {author.name} (ID: {author.id})")
            articles = author.articles()
            if articles:
                print(f"    Articles: {len(articles)}")
                for article in articles[:2]:
                    print(f"      * {article['title']}")
    
    magazines = Magazine.all()
    if magazines:
        print(f"\nSample magazines:")
        for magazine in magazines[:3]:
            print(f"  - {magazine.name} ({magazine.category}) (ID: {magazine.id})")
            articles = magazine.articles()
            if articles:
                print(f"    Articles: {len(articles)}")
    
    print("\n" + "=" * 50)
    print("Starting interactive Python session...")
    print("All classes and functions are available for use.")
    print("Type 'exit()' or Ctrl+D to quit.")
    print("=" * 50)
    
    # Make everything available in the local scope for the interactive session
    import code
    local_vars = {
        'Author': Author,
        'Magazine': Magazine, 
        'Article': Article,
        'add_author_with_articles': add_author_with_articles,
    }
    
    # Add some sample instances if data exists
    if authors:
        local_vars['sample_author'] = authors[0]
    if magazines:
        local_vars['sample_magazine'] = magazines[0]
    
    console = code.InteractiveConsole(locals=local_vars)
    console.interact()

if __name__ == "__main__":
    main()