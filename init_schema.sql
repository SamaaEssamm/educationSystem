CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TYPE user_role AS ENUM ('student', 'admin');

CREATE TABLE users (
  users_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(), 
  users_name TEXT NOT NULL, 
  users_email TEXT UNIQUE NOT NULL, 
  users_role user_role NOT NULL DEFAULT 'student', 
  users_created_at TIMESTAMP DEFAULT NOW(),
  password TEXT
);
