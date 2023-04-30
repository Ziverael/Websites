DROP TABLE IF EXISTS users;

CREATE TABLE users(
    id SMALLINT AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    sex ENUM('Male', 'Female'),
    confirmed BIT(1) COMMENT "Respond for confirmation email",
    
    PRIMARY KEY (id)

)ENGINE = InnoDB, CHARACTER SET = utf8mb4, COLLATE = utf8mb4_polish_ci;