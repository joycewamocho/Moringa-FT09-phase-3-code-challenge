from database.connection import get_db_connection
from models.article import Article
from models.author import Author

class Magazine:
    def __init__(self, id, name="", category=""):
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the magazine already exists
        cursor.execute("SELECT * FROM magazines WHERE id = ? LIMIT 1", [id])
        magazine = cursor.fetchone()

        if magazine:
            self._id = magazine['id']
            self._name = magazine['name']
            self._category = magazine['category']
        else:
            # Insert new magazine if it doesn't exist
            cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (name, category))
            conn.commit()
            self._id = cursor.lastrowid
            self._name = name
            self._category = category

        cursor.close()
        conn.close()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        raise ValueError("ID is immutable and cannot be changed.")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string.")
        if len(value) < 2 or len(value) > 16:
            raise ValueError("Name must be between 2 and 16 characters.")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE magazines SET name = ? WHERE id = ?", (value, self._id))
        conn.commit()
        cursor.close()
        conn.close()

        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str):
            raise TypeError("Category must be a string.")
        if len(value) < 1:
            raise ValueError("Category must not be empty.")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE magazines SET category = ? WHERE id = ?", (value, self._id))
        conn.commit()
        cursor.close()
        conn.close()

        self._category = value

    def contributors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT author_id FROM articles WHERE magazine_id = ?", [self._id])
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        return [Author(row['author_id']) for row in rows]

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM articles WHERE magazine_id = ?", [self._id])
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        return [Article(row['id']) for row in rows]

    def article_titles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", [self._id])
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        return [row["title"] for row in rows] if rows else None

    def contributing_authors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.*, COUNT(DISTINCT m.id) AS magazine_count
            FROM authors a
            JOIN articles ar ON ar.author_id = a.id
            JOIN magazines m ON m.id = ar.magazine_id
            WHERE m.id = ?
            GROUP BY a.id
            HAVING magazine_count > 2
        ''', [self._id])
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        return [Author(row["id"]) for row in rows]

    def __repr__(self):
        return f'<Magazine {self._id}|{self._name}|{self._category}>'
