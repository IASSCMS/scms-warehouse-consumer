-- Create schema
CREATE SCHEMA IF NOT EXISTS oltp;

-- Create a single orders table with nullable warehouse_id
CREATE TABLE oltp.orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity NUMERIC NOT NULL,
    warehouse_id INT,  -- initially NULL, assigned by consumer
    order_date TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'PENDING',
    preferred_delivery_date TIMESTAMPTZ
);

-- Insert hardcoded sample orders with warehouse_id as NULL
INSERT INTO oltp.orders (customer_id, product_id, quantity, preferred_delivery_date)
VALUES
(201, 101, 20, now() + interval '3 days'),
(202, 101, 15, now() + interval '2 days'),
(203, 101, 25, now() + interval '5 days'),
(204, 101, 30, now() + interval '1 days');
