import { CinemaRoom } from '@/models/cinema-room.model';

export interface CinemaRoomRow {
  id?: number;
  cinema_room: CinemaRoom;
  rowNumber: number;
}
