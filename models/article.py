from database.connection import get_db_connection

class Article:
    def __init__(self, id, title="", content="", author_id=0, magazine_id=0):
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ? LIMIT 1", [id])
        article = cursor.fetchone()

        if article:
            self._id = article['id']
            self._title = article['title']
            self._content = article['content']
            self._author_id = article['author_id']
            self._magazine_id = article['magazine_id']
        else:
            # Create an article
            self._id = 0
            self.title = title
            self.magazine_id = magazine_id
            self.author_id = author_id
            self.content = content

            cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)', 
                           (title, content, author_id, magazine_id,))
            self._id = cursor.lastrowid  # Fetch the id of the newly created article
            conn.commit()

        cursor.close()

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        if hasattr(self, "_id"):
            raise ValueError("ID already set")
        
        if not isinstance(id, int):
            raise TypeError("ID must be int")
        
        self._id = id

    @property
    def author_id(self):
        return self._author_id
    
    @author_id.setter
    def author_id(self, author_id):
        if hasattr(self, "_author_id"):
            raise ValueError("Author ID already set")
        
        if not isinstance(author_id, int):
            raise TypeError("Author ID must be int")
        
        self._author_id = author_id

    @property
    def magazine_id(self):
        return self._magazine_id
    
    @magazine_id.setter
    def magazine_id(self, magazine_id):
        if hasattr(self, "_magazine_id"):
            raise ValueError("Magazine ID already set")
        
        if not isinstance(magazine_id, int):
            raise TypeError("Magazine ID must be int")
        
        self._magazine_id = magazine_id

    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, title):
        if hasattr(self, "_title"):
            raise ValueError("Title already set")
        if not isinstance(title, str):
            raise TypeError("Title must be string")
        if len(title) < 5 or len(title) > 50:
            raise ValueError("Title must be between 5 and 50 characters")
        self._title = title


    @property
    def content(self):
        return self._content
    
    @content.setter
    def content(self, content):
        if not isinstance(content, str):
            raise TypeError("Content must be string")
        
        if len(content) > 5000:
            raise ValueError("Content must be less than 5000 characters")
        
        # Connect to the database and update content
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE articles SET content = ? WHERE id = ? LIMIT 1", (content, self.id,))
        conn.commit()
        cursor.close()

        self._content = content

    def _get_record_by_id(self, table, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT id FROM {table} WHERE id = ? LIMIT 1", [id])
        record = cursor.fetchone()
        conn.close()
        return record

    @property
    def author(self):
        author = self._get_record_by_id("authors", self.author_id)
        if author:
            return Author(author["id"])
        return None
    
    @property
    def magazine(self):
        magazine = self._get_record_by_id("magazines", self.magazine_id)
        if magazine:
            return Magazine(magazine["id"])
        return None

    def __repr__(self):
        return f'<Article ID:{self.id}, Title:{self.title} Author ID:{self.author_id} Magazine ID:{self.magazine_id}|{self.content}>'
