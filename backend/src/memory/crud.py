from memory.database import get_connection
from models.user import User
from models.message import Message
from models.chat import Chat

# ----- MESSAGE -----

def create_message(message: Message):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO messages (chat_id, message_role, content) 
        VALUES (?, ?, ?)
    """, (message.chat_id, message.role, message.content, ))

    message.id = cursor.lastrowid
    conn.commit()
    conn.close()

    return message

def delete_message(id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM messages
        WHERE id = ?
    """, (id, ))

    conn.commit()
    conn.close()

def get_all_messages(chat_id: int): 
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * 
        FROM messages
        WHERE chat_id = ?
        ORDER BY created_at ASC
    """, (chat_id, ))

    rows = cursor.fetchall()
    conn.close()

    return [Message.from_row(row) for row in rows]

# ----- CHAT -----

def create_chat(chat: Chat):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO chats (user_id, title)
        VALUES (?, ?)
    """, (chat.user_id, chat.title, ))

    chat.id = cursor.lastrowid
    conn.commit()
    conn.close()

    return chat

def update_chat_title(chat: Chat):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE chats
        SET title = ?
        WHERE id = ?
    """, (chat.title, chat.id, ))

    conn.commit()
    conn.close()

def delete_chat(id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM chats
        WHERE id = ?
    """, (id, ))

    conn.commit()
    conn.close()

def get_all_chats(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM chats
        WHERE user_id = ?
    """, (user_id, ))

    rows = cursor.fetchall()
    conn.close()

    return [Chat.from_row(row) for row in rows]

# ----- USER -----

def create_user(user: User):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (username, password_hash, user_role)
        VALUES (?, ?, ?)
    """, (user.name, user.password_hash, user.role, ))

    user.id = cursor.lastrowid
    conn.commit()
    conn.close()

    return user

def update_user_role(user: User): 
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET user_role = ?
        WHERE id = ?
    """, (user.role, user.id))

    conn.commit()
    conn.close()

def update_user_password(user: User):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET password_hash = ? 
        WHERE id = ?
    """, (user.password_hash, user.id))

    conn.commit()
    conn.close()

def delete_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM users
        WHERE id = ?
    """, (user_id, ))

    conn.commit()
    conn.close()

# ----- ROLE PERMISSIONS -----

def grant_table_permission(role: str, table_name: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO role_permissions (permission_role, table_name)
        VALUES (?, ?)
    """, (role, table_name, ))

    conn.commit()
    conn.close()

def revoke_allower_table(role: str, table_name: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM role_permissions
        WHERE permission_role = ? AND table_name = ?
    """, (role, table_name))

    conn.commit()
    conn.close()

def get_allowed_tables(role: str) -> list[str]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT table_name
        FROM role_permissions
        WHERE permission_role = ?
    """, (role, ))

    rows = cursor.fetchall()
    conn.close()

    return [row["table_name"] for row in rows]