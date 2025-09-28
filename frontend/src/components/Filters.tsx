import { Button } from "@/components/ui/button";
import { MovieGenre } from "@/models/movie-genre.model";

interface FiltersProps {
  genres: MovieGenre[];
  selectedGenres: string[];
  onFilterChange: (selectedGenres: string[]) => void;
}

const Filters = ({ genres, selectedGenres, onFilterChange }: FiltersProps) => {
  const toggleGenre = (genreName: string) => {
    if (selectedGenres.includes(genreName)) {
      onFilterChange(selectedGenres.filter((g) => g !== genreName));
    } else {
      onFilterChange([...selectedGenres, genreName]);
    }
  };

  return (
    <div className="flex gap-2 mt-4 overflow-x-auto">
      {genres.map((genre) => (
        <Button
          key={genre.id}
          variant={selectedGenres.includes(genre.name) ? "default" : "outline"}
          size="sm"
          onClick={() => toggleGenre(genre.name)}
        >
          {genre.name}
        </Button>
      ))}
    </div>
  );
};

export default Filters;
