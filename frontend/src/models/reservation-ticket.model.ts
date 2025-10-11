import { CinemaRoomSeat } from "@/models/cinema-room-seat.model";
import { TicketType } from "@/models/ticket-type.model";

export interface Reservation {
  id?: number;
  uuid?: string | null;
  secret: string;
  reservation?: Reservation["id"];
  cinema_room_seat?: CinemaRoomSeat["id"] | null;
  ticket_type?: TicketType["id"] | null;
}
