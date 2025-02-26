CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,   -- 用户ID，自增主键
    username VARCHAR(255) NOT NULL UNIQUE,    -- 用户名，唯一
    hashed_password VARCHAR(255) NOT NULL     -- 哈希后的密码
);