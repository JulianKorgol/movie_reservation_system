import { TicketType } from "@/models/ticket-type.model";

export interface CinemaRoomSeat {
  id?: number;
  seat_number: number;
  status: 0 | 1; // 0 - broken, 1 - working
  seat_type?: TicketType | null;
}
