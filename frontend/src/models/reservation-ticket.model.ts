import { CinemaRoomSeat } from "@/models/cinema-room-seat.model";
import { TicketType } from "@/models/ticket-type.model";

export interface Reservation {
  id?: string;
  uuid?: string | null;
  secret: string;
  reservation?: Reservation;
  cinema_room_seat?: CinemaRoomSeat | null;
  ticket_type?: TicketType | null;
}
