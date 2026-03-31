-- Restaurants table (stores all restaurants, visited or not)
CREATE TABLE restaurants (
    restaurant_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    cuisine VARCHAR(50),
    city VARCHAR(100),
    state VARCHAR(50),
    price_level INT,          -- 1 = cheap, 2 = medium, 3 = expensive
    has_visited BOOLEAN DEFAULT FALSE,
    notes TEXT
);

-- Visits table (each time you go to a restaurant)
CREATE TABLE visits (
    visit_id INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_id INT,
    visit_date DATE,
    total_spent DECIMAL(8,2),
    notes TEXT,
    
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id)
);

-- Menu items table (items offered at each restaurant)
CREATE TABLE menu_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_id INT,
    item_name VARCHAR(100),
    price DECIMAL(6,2),
    
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id)
);

-- Orders table (what you ordered during a visit)
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    visit_id INT,
    item_id INT,
    quantity INT DEFAULT 1,
    
    FOREIGN KEY (visit_id) REFERENCES visits(visit_id),
    FOREIGN KEY (item_id) REFERENCES menu_items(item_id)
);

-- Ratings table (rate restaurants or specific visits)
CREATE TABLE ratings (
    rating_id INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_id INT,
    visit_id INT,
    food_rating INT,
    service_rating INT,
    overall_rating INT,
    
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id),
    FOREIGN KEY (visit_id) REFERENCES visits(visit_id)
);