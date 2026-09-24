import sqlite3

conn = sqlite3.connect('timetables.db', check_same_thread=False)
conn.row_factory = sqlite3.Row
csr = conn.cursor()
csr.execute('PRAGMA foreign_keys = ON')

def init_db():
    csr.execute('''CREATE TABLE IF NOT EXISTS classes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        branch TEXT NOT NULL,
        section TEXT NOT NULL,
        day_of_week TEXT NOT NULL,
        class_order INTEGER NOT NULL,
        class_name TEXT NOT NULL,
        sesmester INTEGER NOT NULL DEFAULT 1,
        UNIQUE(branch, section, day_of_week, class_order)
    )''')
    conn.commit()

def class_add(class_name, branch, section, day, order):
    csr.execute('''INSERT INTO classes(class_name, branch, section, day_of_week, class_order)
        VALUES (?,?,?,?,?)''', (class_name, branch, section, day, order))
    conn.commit()

def class_edit(class_id, class_name):
    csr.execute('UPDATE classes SET class_name = ? WHERE id = ?', (class_name, class_id))
    conn.commit()

def class_delete(class_id):
    csr.execute('DELETE FROM classes WHERE id = ?', (class_id,))
    conn.commit()

def get_timetable(branch, section):
    return csr.execute('''SELECT id, day_of_week, class_order, class_name, branch, section FROM classes
        WHERE branch = ? AND section = ? ORDER BY class_order''',
        (branch, section)).fetchall()