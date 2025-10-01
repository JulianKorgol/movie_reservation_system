import { CinemaRoom } from '@/models/cinema-room.model';
import { Movie } from '@/models/movie.model';

export interface Showtime {
  id?: string;
  movie?: Movie | null;
  start_time: string;
  end_time: string;
  cinema_room?: CinemaRoom | null;
}
