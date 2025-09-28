import {
  Card,
  CardFooter,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Movie } from "@/models/movie.model";
import Link from "next/link";

const MovieCard = ({ movie }: { movie: Movie }) => (
  <Card className="flex flex-col h-full overflow-hidden">
    <div className="w-full aspect-[2/3] overflow-hidden">
      <img
        src={movie.image_path ?? "/placeholder.jpg"}
        alt={movie.title}
        className="w-full h-full object-cover"
      />
    </div>

    <CardHeader className="p-4">
      <CardTitle className="text-lg md:text-xl">{movie.title}</CardTitle>
      <CardDescription className="text-sm text-gray-500 dark:text-gray-400">
        {movie.genre?.name}
      </CardDescription>
    </CardHeader>

    <CardFooter className="p-4 mt-auto">
      <Button variant="default" className="w-full">
        <Link href={`/movies/${movie.url}`}>Book Now</Link>
      </Button>
    </CardFooter>
  </Card>
);

export default MovieCard;
