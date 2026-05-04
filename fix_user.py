import sqlite3
import bcrypt  # Built-in dependency

conn = sqlite3.connect('task_manager.db')
conn.execute('DELETE FROM users')
conn.commit()

print("🔐 Creating users with PROPER bcrypt hashes...")

# Admin with hashed password
admin_pass = b'123123123'
admin_hash = bcrypt.hashpw(admin_pass, bcrypt.gensalt()).decode()
john_pass = b'john123'
john_hash = bcrypt.hashpw(john_pass, bcrypt.gensalt()).decode()

conn.execute('INSERT INTO users (username, email, hashed_password, role) VALUES (?, ?, ?, ?)', 
             ('admin1', 'admin1@gmail.com', admin_hash, 'admin'))
conn.execute('INSERT INTO users (username, email, hashed_password, role) VALUES (?, ?, ?, ?)', 
             ('john', 'john@team.com', john_hash, 'member'))

conn.commit()

print("\n✅ USERS WITH HASHES:")
for row in conn.execute('SELECT id, username, email, role FROM users'):
    print(f"  ID:{row[0]} {row[1]} ({row[3]}) - {row[2]}")

print("\n🎉 LOGIN:")
print("   Email: admin1@gmail.com")
print("   Password: 123123123")
print("   Email: john@team.com")
print("   Password: john123")
conn.close()