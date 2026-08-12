CREATE TABLE flight_info (
    id INTEGER,
    source VARCHAR(50),
    destination VARCHAR(50)
);

INSERT INTO flight_info (id, source, destination) VALUES
(1, 'Delhi', 'Kolkata'),
(2, 'Kolkata', 'Banglore'),
(3, 'Mumbai', 'Pune'),
(4, 'Pune', 'Goa'),
(5, 'Kolkata', 'Delhi'),
(6, 'Delhi', 'Srinagar');
