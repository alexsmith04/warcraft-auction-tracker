CREATE TABLE IF NOT EXISTS item_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    median_price INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    timestamp DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS items (
    item_id INTEGER PRIMARY KEY,
    name TEXT,
    last_updated TEXT
);
