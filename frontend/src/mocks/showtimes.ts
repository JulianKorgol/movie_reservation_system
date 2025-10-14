import { mockMovies } from "@/mocks/movies";
import { Showtime } from "@/models/showtime.model";
import moment from "moment";

export const showtimes: Showtime[] = [
  {
    id: 1,
    movie: mockMovies[0].id,
    start_time: moment().add(1, "days").set({ hour: 14, minute: 0, second: 0 }).toISOString(),
    end_time: moment().add(1, "days").set({ hour: 16, minute: 0, second: 0 }).toISOString(),
    cinema_room: 1,
  },
  {
    id: 2,
    movie: mockMovies[1].id,
    start_time: moment().add(1, "days").set({ hour: 17, minute: 0, second: 0 }).toISOString(),
    end_time: moment().add(1, "days").set({ hour: 19, minute: 0, second: 0 }).toISOString(),
    cinema_room: 2,
  },
  {
    id: 3,
    movie: mockMovies[2].id,
    start_time: moment().add(2, "days").set({ hour: 15, minute: 30, second: 0 }).toISOString(),
    end_time: moment().add(2, "days").set({ hour: 17, minute: 30, second: 0 }).toISOString(),
    cinema_room: 1,
  },
  {
    id: 4,
    movie: mockMovies[3].id,
    start_time: moment().add(2, "days").set({ hour: 18, minute: 0, second: 0 }).toISOString(),
    end_time: moment().add(2, "days").set({ hour: 20, minute: 0, second: 0 }).toISOString(),
    cinema_room: 3,
  },
];
