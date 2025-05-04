-- Create schema
CREATE SCHEMA IF NOT EXISTS oltp;

-- Create warehouse table
CREATE TABLE oltp.warehouse (
    warehouse_id SERIAL PRIMARY KEY,
    location_x NUMERIC,
    location_y NUMERIC,
    warehouse_name VARCHAR,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Create warehouse_inventory table
CREATE TABLE oltp.warehouse_inventory (
    inventory_id SERIAL PRIMARY KEY,
    warehouse_id INT REFERENCES oltp.warehouse(warehouse_id),
    product_id INT,
    supplier_id INT,
    quantity NUMERIC,
    last_restocked TIMESTAMPTZ,
    minimum_stock_level NUMERIC,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Insert 5 fixed warehouses with numeric coordinates
INSERT INTO oltp.warehouse (location_x, location_y, warehouse_name) VALUES
(10.0, 20.0, 'Warehouse A'),
(15.0, 25.0, 'Warehouse B'),
(30.0, 35.0, 'Warehouse C'),
(40.0, 10.0, 'Warehouse D'),
(50.0, 50.0, 'Warehouse E');

-- Insert inventory for the same product_id = 101 in all warehouses
INSERT INTO oltp.warehouse_inventory (
    warehouse_id, product_id, supplier_id, quantity, last_restocked, minimum_stock_level
) VALUES
(1, 101, 501, 50, now() - interval '5 days', 10),
(2, 101, 501, 40, now() - interval '10 days', 8),
(3, 101, 501, 60, now() - interval '3 days', 12),
(4, 101, 501, 55, now() - interval '7 days', 15),
(5, 101, 501, 70, now() - interval '1 days', 9);
