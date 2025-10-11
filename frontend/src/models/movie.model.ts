import { MovieGenre } from "@/models/movie-genre.model";

export interface Movie {
  id?: number;
  title: string;
  description?: string | null;
  genre?: MovieGenre | null;
  image_path?: string | null;
  url: string;
}
