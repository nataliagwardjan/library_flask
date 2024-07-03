"""
TABLES:
    users - users of application
    roles - roles for all users (from enum class)
    titles - titles of books available in the library
    copies - copies of titles available in the library
    categories - type/category of book (from enum class)
    authors - authors of books
    titles_categories - table connecting titles with categories
    copy_statuses - table with possible copy statuses
    users_roles - table connecting users with their roles
"""
from main.const.database_const import TABLE_USERS, TABLE_ROLES, TABLE_USERS_ROLES, TABLE_TITLES_CATEGORIES, \
    TABLE_CATEGORIES, TABLE_STATUSES

create_users_table = f"""
    -- users table
    CREATE TABLE IF NOT EXISTS {TABLE_USERS} (
    id TEXT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password TEXT
    );
"""

create_roles_table = f"""
    -- roles table
    CREATE TABLE IF NOT EXISTS {TABLE_ROLES} (
    id TEXT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
    );
"""

create_users_roles_table = f"""
    -- roles table
    CREATE TABLE IF NOT EXISTS {TABLE_USERS_ROLES} (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    role_id TEXT,
    FOREIGN KEY (user_id) REFERENCES {TABLE_USERS}(id)
    FOREIGN KEY (role_id) REFERENCES {TABLE_ROLES}(id)
    );
"""

create_categories_table = f"""
    -- categories table
    CREATE TABLE IF NOT EXISTS {TABLE_CATEGORIES} (
    id TEXT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
    );
"""

create_statuses_table = f"""
    -- statuses table
    CREATE TABLE IF NOT EXISTS {TABLE_STATUSES} (
    id TEXT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
    );
"""

insert_user_sql = f"""
INSERT INTO {TABLE_USERS} (id, name, surname, email, password) VALUES (?, ?, ?, ?, ?)
"""

insert_user_role_sql = f"""
INSERT INTO {TABLE_USERS_ROLES} (id, user_id, role_id) VALUES (?, ?, ?)
"""

insert_titles_categories_sql = f"""
INSERT INTO {TABLE_TITLES_CATEGORIES} (id, title_id, category_id) VALUES (?, ?, ?)
"""
