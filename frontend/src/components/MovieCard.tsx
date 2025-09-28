import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Movie } from "@/models/movie.model";

{
  /* for later use
const description = (movie: Movie) => {
  if (movie.description != null && movie.description.length > 100) {
    const truncated = movie.description.slice(0, 100);
    const lastSpace = truncated.lastIndexOf(" ");
    return (lastSpace > 0 ? truncated.slice(0, lastSpace) : truncated) + "...";
  }
  return movie.description;
};
*/
}

const MovieCard = ({ movie }: { movie: Movie }) => (
  <Card className="overflow-hidden flex flex-col">
    <img
      src={movie.image_path ?? ""}
      alt={movie.title}
      className="w-full object-cover"
    />
    <CardHeader>
      <CardTitle>{movie.title}</CardTitle>
      <CardDescription>{movie.genre?.name}</CardDescription>
    </CardHeader>
    <CardContent className="mt-auto">
      {/*<p className="text-sm text-gray-600 dark:text-gray-400">*/}
      {/*  {description(movie)}*/}
      {/*</p>*/}
    </CardContent>
    <CardFooter>
      <Button variant="default" className="w-full">
        Book Now
      </Button>
    </CardFooter>
  </Card>
);

export default MovieCard;
