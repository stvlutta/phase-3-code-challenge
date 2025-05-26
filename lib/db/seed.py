import os
import sys

# Add the lib directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def seed_database():
    """Populate the database with test data"""
    
    print("Seeding database with test data...")
    
    # Create authors
    author1 = Author("John Doe").save()
    author2 = Author("Jane Smith").save()
    author3 = Author("Mike Johnson").save()
    
    print(f"Created authors: {author1.name}, {author2.name}, {author3.name}")
    
    # Create magazines
    magazine1 = Magazine("Tech Weekly", "Technology").save()
    magazine2 = Magazine("Science Today", "Science").save()
    magazine3 = Magazine("Health & Wellness", "Health").save()
    
    print(f"Created magazines: {magazine1.name}, {magazine2.name}, {magazine3.name}")
    
    # Create articles
    articles_data = [
        ("The Future of AI", author1.id, magazine1.id),
        ("Machine Learning Basics", author2.id, magazine1.id),
        ("Quantum Computing Explained", author1.id, magazine2.id),
        ("Climate Change Solutions", author3.id, magazine2.id),
        ("Healthy Living Tips", author2.id, magazine3.id),
        ("Exercise and Mental Health", author1.id, magazine3.id),
        ("Advanced Python Techniques", author2.id, magazine1.id),
        ("Data Science Trends", author3.id, magazine1.id),
        ("Nutrition Fundamentals", author3.id, magazine3.id),
    ]
    
    created_articles = []
    for title, author_id, magazine_id in articles_data:
        article = Article(title, author_id, magazine_id).save()
        created_articles.append(article)
    
    print(f"Created {len(created_articles)} articles")
    
    # Display some statistics
    print("\n--- Database Statistics ---")
    print(f"Total authors: {len(Author.all())}")
    print(f"Total magazines: {len(Magazine.all())}")
    print(f"Total articles: {len(Article.all())}")
    
    # Show author-magazine relationships
    print("\n--- Author-Magazine Relationships ---")
    for author in Author.all():
        magazines = author.magazines()
        magazine_names = [mag['name'] for mag in magazines]
        print(f"{author.name} has written for: {', '.join(magazine_names) if magazine_names else 'No magazines'}")
    
    print("\nDatabase seeding completed!")

if __name__ == "__main__":
    seed_database()