USE BGsessions;
DROP TABLE IF EXISTS users;

CREATE TABLE users(
    id SMALLINT AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    votes SMALLINT DEFAULT 0,
    confirmed BIT(1) COMMENT "Respond for confirmation email",
    accepted BIT(1) DEFAULT 0 COMMENT "If admin accepted request to join",
    PRIMARY KEY (id)

)ENGINE = InnoDB, CHARACTER SET = utf8mb4, COLLATE = utf8mb4_polish_ci;