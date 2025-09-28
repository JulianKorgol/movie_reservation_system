import { Movie } from "@/models/movie.model";
import { CinemaRoom } from "@/models/cinema-room.model";

export interface Showtime {
  id?: string;
  movie?: Movie | null;
  start_time: string;
  end_time: string;
  cinema_room?: CinemaRoom | null;
}
