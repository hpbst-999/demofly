\c demo
ALTER ROLE database_user SET search_path TO bookings;
CREATE INDEX IF NOT EXISTS idx_tickets_passenger_name ON tickets (passenger_name);
CREATE INDEX IF NOT EXISTS idx_boarding_passes_no_text ON boarding_passes ((boarding_no::text));
CREATE INDEX IF NOT EXISTS idx_segments_flight_id_text ON segments ((flight_id::text));
CREATE INDEX IF NOT EXISTS idx_tickets_book_ref_join ON tickets (book_ref);
CREATE INDEX IF NOT EXISTS idx_segments_ticket_no_join ON segments (ticket_no);
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user'
);
INSERT INTO users (username, password_hash, role) VALUES 
('admin', '$2b$12$kYLYjYeEXkotz/kRjTSgg.532sDEHmHv86qTil09qGWiwTK0eZaJK', 'admin'),
('user', '$2b$12$QUuUcc5GRT8J7rGtrnQ1gueF.cvC3Fci9RxKu5wEqS9cuzHSlcR0O', 'user')
ON CONFLICT (username) DO NOTHING;