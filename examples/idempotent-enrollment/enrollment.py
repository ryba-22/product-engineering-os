"""Small local example: atomic enrollment uniqueness using SQLite."""
import sqlite3

def connect():
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE enrollment (pupil TEXT, course TEXT, UNIQUE(pupil, course))")
    return db

def enroll(db, pupil, course):
    if not isinstance(pupil, str) or not pupil.strip():
        raise ValueError("pupil is required")
    if not isinstance(course, str) or not course.strip():
        raise ValueError("course is required")
    with db:
        cursor = db.execute("INSERT OR IGNORE INTO enrollment VALUES (?, ?)", (pupil.strip(), course.strip()))
    return "created" if cursor.rowcount else "already_enrolled"
