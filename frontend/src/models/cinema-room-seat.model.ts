import { TicketType } from "@/models/ticket-type.model";
import { CinemaRoomRow } from "./cinema-room-row.model";

export interface CinemaRoomSeat {
  id?: number;
  seat_number: number;
  row: CinemaRoomRow["id"];
  status: 0 | 1; // 0 - broken, 1 - working
  seat_type?: TicketType["id"] | null;
}
