import { MovieGenre } from "@/models/movie-genre.model";

export interface Movie {
  id?: string;
  title: string;
  description?: string | null;
  genres?: MovieGenre | null;
  image_path?: string | null;
  url: string;
}
