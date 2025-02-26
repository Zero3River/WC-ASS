CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,  
    username VARCHAR(255) NOT NULL UNIQUE,    
    hashed_password VARCHAR(255) NOT NULL
);