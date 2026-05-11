ALTER ROLE db_user SET search_path TO bookings;
CREATE INDEX IF NOT EXISTS idx_tickets_passenger_name ON tickets (passenger_name);
CREATE INDEX IF NOT EXISTS idx_boarding_passes_no_text ON boarding_passes ((boarding_no::text));
CREATE INDEX IF NOT EXISTS idx_segments_flight_id_text ON segments ((flight_id::text));
CREATE INDEX IF NOT EXISTS idx_tickets_book_ref_join ON tickets (book_ref);
CREATE INDEX IF NOT EXISTS idx_segments_ticket_no_join ON segments (ticket_no);