class AdminService:
    pattern_num = r"^\d{13}$"
    pattern_code_num = r"^[A-Z]{2}\s\d{13}$"
    pattern_time = r'\d{2}:\d{2}:\d{2}'
    entities = {
    "tables": [
      {"name": "bookings"},
      {"name": "tickets"},
      {"name": "boarding_passes"},
      {"name": "segments"},
      {"name": "flights"},
      {"name": "routes"},
      {"name": "airports"},
      {"name": "airplanes"},
      {"name": "seats"}
            ]}

    ALLOWED_TABLES = [
        "bookings", "tickets", "boarding_passes",
        "segments", "flights", "routes",
        "airports", "airplanes", "seats"
    ]
    TABLE_KEYS = {
    "bookings": "book_ref",
    "tickets": "ticket_no",
    "flights": "flight_id",
    "airports": "airport_code",
    "airplanes": "airplane_code",
    "routes": ["route_no","airplane_code"], 
    "boarding_passes": ["ticket_no", "flight_id"],
    "seats": ["airplane_code", "seat_no"],
    "segments": ["flight_id", "ticket_no"]
}
    def serialize_row_safe(self,row):

        result = {}
        for key, value in row.items():
            if value is None:
                result[key] = None
            elif isinstance(value, psycopg2.extras.Range):
                result[key] = f"[{value.lower},{value.upper})"
            elif isinstance(value, (datetime.time, datetime.datetime)):
                result[key] = value.isoformat()
            elif isinstance(value, datetime.timedelta):
                total_seconds = int(value.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                seconds = total_seconds % 60
                result[key] = f"{hours:02}:{minutes:02}:{seconds:02}"
            else:
                result[key] = value
        return result