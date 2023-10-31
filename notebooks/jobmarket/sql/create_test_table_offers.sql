CREATE TABLE ofertas_jobmarket_canarias_21_23 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    description TEXT NOT NULL,
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255),
    location VARCHAR(255),
    category VARCHAR(255),
    jobType VARCHAR(255),
    salaryOriginal VARCHAR(255),
    numberOfVacancies INT
);