"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { mockMovies } from "@/mocks/movies";
import { showtimes } from "@/mocks/showtimes";
import MovieDetailsSkeleton from "@/components/MovieDetailsSkeleton";
import ShowtimeCard from "@/components/ShowtimeCard";

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";

export default function MoviePage() {
  const { slug } = useParams();
  const [movie, setMovie] = useState<(typeof mockMovies)[0] | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setTimeout(() => {
      const foundMovie = mockMovies.find((m) => m.url === slug) || null;
      setMovie(foundMovie);
      setIsLoading(false);
    }, 1000);
  }, [slug]);

  if (isLoading) return <MovieDetailsSkeleton />;
  if (!movie) return <div className="p-6 text-center">Movie not found</div>;

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <Card className="flex flex-col md:flex-row overflow-hidden">
        <img
          src={movie.image_path ?? ""}
          alt={movie.title}
          className="w-full md:w-1/2 h-full object-cover rounded-md"
        />

        <CardContent className="flex flex-col justify-between p-6 md:w-1/2">
          <div>
            <CardHeader className="p-0">
              <CardTitle className="text-3xl">{movie.title}</CardTitle>
              <CardDescription className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                {movie.genre?.name}
              </CardDescription>
            </CardHeader>
            <p className="mt-4 text-gray-700 dark:text-gray-300">
              {movie.description}
            </p>
          </div>

          <div
            className="mt-6 flex flex-col gap-4 max-h-100 overflow-y-auto pr-2"
            style={{ scrollbarWidth: "thin" }}
          >
            {showtimes
              .filter((showtime) => showtime.movie.id === movie.id)
              .map((showtime) => (
                <ShowtimeCard
                  key={showtime.id}
                  cinemaName="Cinema City"
                  roomNumber={showtime.cinema_room.name}
                  startTime={showtime.start_time}
                  endTime={showtime.end_time}
                  availableSeats={showtime.cinema_room.capacity}
                  onBook={() =>
                    toast.success("Booking successful!", {
                      description: `You have booked a seat for ${movie.title} at ${showtime.start_time}.`,
                    })
                  }
                />
              ))}
          </div>

          <Button variant="default" className="mt-6 w-full self-start">
            Book Now
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
