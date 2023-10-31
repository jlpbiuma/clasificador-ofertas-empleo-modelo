CREATE TABLE postings_jobmarket_canarias_21_23 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_posting VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    url VARCHAR(255) NOT NULL,
    titleOriginal VARCHAR(255) NOT NULL,
    site VARCHAR(255) NOT NULL,
    salaryOriginal DECIMAL(10, 2)
);