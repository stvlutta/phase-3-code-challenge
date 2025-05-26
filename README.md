# Phase 3 Code Challenge - Articles Management System

A Python application for managing authors, magazines, and articles with SQLite database backend. This system demonstrates object-relational mapping (ORM) patterns and database relationships.

## Features

- **Author Management**: Create and manage authors with their articles and publications
- **Magazine Management**: Organize magazines by categories and track contributors  
- **Article Management**: Link articles to authors and magazines with full CRUD operations
- **Relationship Queries**: Find articles by author, magazines by contributor, topic areas, and more
- **Analytics**: Identify top publishers, contributing authors, and publication statistics

## Database Schema

The application uses three main entities:

- **Authors**: Store author information (id, name)
- **Magazines**: Store magazine details (id, name, category) 
- **Articles**: Link authors and magazines (id, title, author_id, magazine_id)

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd phase-3-code-challenge
   ```

2. **Set up the database**:
   ```bash
   python scripts/setup_db.py
   ```

3. **Seed with test data** (optional):
   ```bash
   python lib/db/seed.py
   ```

## Usage

### Run Example Queries
```bash
python scripts/run_queries.py
```

### Working with Models

```python
from lib.models.author import Author
from lib.models.magazine import Magazine  
from lib.models.article import Article

# Create an author
author = Author("John Doe").save()

# Create a magazine
magazine = Magazine("Tech Weekly", "Technology").save()

# Create an article
article = Article("AI Revolution", author.id, magazine.id).save()

# Find relationships
author_articles = author.articles()
magazine_contributors = magazine.contributors()
author_topics = author.topic_areas()
```

## Available Methods

### Author Methods
- `save()` - Create/update author
- `find_by_id(id)` - Find author by ID
- `find_by_name(name)` - Find author by name
- `all()` - Get all authors
- `articles()` - Get author's articles
- `magazines()` - Get magazines author has written for
- `topic_areas()` - Get categories author has written about
- `add_article(magazine, title)` - Create new article

### Magazine Methods  
- `save()` - Create/update magazine
- `find_by_id(id)` - Find magazine by ID
- `find_by_name(name)` - Find magazine by name
- `find_by_category(category)` - Find magazines by category
- `all()` - Get all magazines
- `articles()` - Get magazine's articles
- `contributors()` - Get magazine's contributors
- `article_titles()` - Get list of article titles
- `contributing_authors()` - Get authors with >2 articles
- `top_publisher()` - Get magazine with most articles

### Article Methods
- `save()` - Create/update article  
- `find_by_id(id)` - Find article by ID
- `find_by_title(title)` - Find articles by title
- `find_by_author(author_id)` - Find articles by author
- `find_by_magazine(magazine_id)` - Find articles by magazine
- `all()` - Get all articles
- `author()` - Get article's author
- `magazine()` - Get article's magazine

## Testing

Run the test suite:
```bash
python -m pytest tests/
```

The application includes comprehensive tests for all models and their relationships.

## Project Structure

```
phase-3-code-challenge/
├── lib/
│   ├── models/          # Model classes
│   │   ├── author.py
│   │   ├── magazine.py
│   │   └── article.py
│   └── db/              # Database utilities
│       ├── connection.py
│       ├── schema.sql
│       ├── seed.py
│       └── transactions.py
├── scripts/             # Utility scripts
│   ├── setup_db.py      # Database setup
│   └── run_queries.py   # Example queries
├── tests/               # Test suite
└── README.md
```

## Requirements

- Python 3.6+
- SQLite3 (included with Python)
- pytest (for testing)

## License

This project is licensed under the MIT License.  
See the [LICENSE](./LICENSE) file for details.
