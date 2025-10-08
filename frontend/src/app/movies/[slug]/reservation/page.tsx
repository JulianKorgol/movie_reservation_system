"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { mockMovies } from "@/mocks/movies";
import { showtimes } from "@/mocks/showtimes";
import MovieDetailsSkeleton from "@/components/MovieDetailsSkeleton";

import { Card, CardContent, CardTitle } from "@/components/ui/card";
import { Icon } from "@iconify/react";
import Seat from "@/components/ui/seat";
import Room from "@/components/Room";
import { roomA } from "@/rooms/roomA";
import { roomB } from "@/rooms/roomB";

export default function ReservationPage() {
  const { slug } = useParams();
  const [movie, setMovie] = useState<(typeof mockMovies)[0] | null>(null);
  const [showtime, setShowtime] = useState<(typeof showtimes)[0] | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setTimeout(() => {
      const foundMovie = mockMovies.find((m) => m.url === slug) || null;

      const foundShowtime = showtimes.find((s) => s.movie === foundMovie) || null;
      setShowtime(foundShowtime);

      setMovie(foundMovie);
      setIsLoading(false);
    }, 1000);
  }, [slug]);

  if (isLoading) return <MovieDetailsSkeleton />;
  if (!movie) return <div className="p-6 text-center">Movie not found</div>;

  return (
    <div className="p-6 max-w-7xl mx-auto h-svh">
      <Card className="flex flex-col md:flex-row overflow-hidden h-full">
        <div className="md:w-1/2 flex flex-col items-center p-4 gap-2">
          <img src={movie.image_path ?? ""} alt={movie.title} className="h-96 object-cover rounded-md" />
          <CardTitle className="text-3xl">{movie.title}</CardTitle>
          <p className="text-gray-700 dark:text-gray-300 max-w-3/4 line-clamp-2 overflow-hidden">{movie.description}</p>
          <p className="text-gray-700 dark:text-gray-400">
            <b>Cinema City</b>, {showtime?.cinema_room.name}
          </p>
          <p className="text-gray-700 dark:text-gray-300 flex items-center gap-1">
            <Icon icon="mdi:clock-time-four-outline" />
            {showtime?.start_time} - {showtime?.end_time}
          </p>
        </div>
        <CardContent className="flex flex-col p-6 md:w-1/2">
          <div className="flex w-full justify-around items-center mb-4">
            <div className="flex items-center gap-2">
              <Seat status="available" number={0} />{" "}
              <span className="text-gray-700 dark:text-gray-400 text-sm">Available</span>
            </div>
            <div className="flex items-center gap-2">
              <Seat status="selected" number={0} />{" "}
              <span className="text-gray-700 dark:text-gray-400 text-sm">Selected</span>
            </div>
            <div className="flex items-center gap-2">
              <Seat status="unavailable" number={0} />{" "}
              <span className="text-gray-700 dark:text-gray-400 text-sm">Unavailable</span>
            </div>
          </div>
          <hr className="my-4" />
          <Room room={roomA} />
        </CardContent>
      </Card>
    </div>
  );
}
