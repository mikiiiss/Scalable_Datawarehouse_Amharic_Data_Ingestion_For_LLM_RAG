CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    image_url TEXT,
    time_publish VARCHAR(50),
    title TEXT,
    article_url TEXT,
    highlight TEXT,
    date_published TIMESTAMP,
    publisher_name VARCHAR(100),
    detail_content TEXT,
    category VARCHAR(50)
);
