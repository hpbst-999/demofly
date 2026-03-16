from dataclasses import dataclass
@dataclass
class Tickets:
    ticket_no: str
    book_ref: str
    passenger_id: str
    passenger_name: str
    outbound: bool

@dataclass
class TicketsDTO:
    ticket_no: str
    book_ref: str
    passenger_id: str
    passenger_name: str
    outbound: str

    @classmethod
    def convert_to_dto(cls, ticket: Tickets) -> 'TicketsDTO':
        return cls(
            ticket_no=str(ticket.ticket_no),
            book_ref=str(ticket.book_ref),
            passenger_id=str(ticket.passenger_id),
            passenger_name=str(ticket.passenger_name),
            outbound=str(ticket.outbound)
        )