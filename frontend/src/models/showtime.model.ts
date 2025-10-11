import { Movie } from "@/models/movie.model";
import { CinemaRoom } from "@/models/cinema-room.model";

export interface Showtime {
  id?: number;
  movie?: Movie["id"] | null;
  start_time: string;
  end_time: string;
  cinema_room?: CinemaRoom["id"] | null;
}
