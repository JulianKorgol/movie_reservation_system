import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";

interface ShowtimeCardProps {
  cinemaName: string;
  roomNumber: string | number;
  startTime: string;
  endTime: string;
  availableSeats: number;
  onBook: () => void;
}

export default function ShowtimeCard({
  cinemaName,
  roomNumber,
  startTime,
  endTime,
  availableSeats,
  onBook,
}: ShowtimeCardProps) {
  return (
    <Card className="flex flex-col md:flex-row justify-between md:items-center p-4 gap-4 hover:shadow-md transition-shadow duration-200">
      <CardContent className="flex-1 p-0">
        <CardHeader className="p-0">
          <CardTitle className="text-lg md:text-xl">
            {cinemaName} (Room {roomNumber})
          </CardTitle>
          <CardDescription className="text-sm text-gray-500 dark:text-gray-400 mt-1">
            {startTime} - {endTime}
          </CardDescription>
        </CardHeader>
        <p className="mt-2 text-sm text-gray-700 dark:text-gray-300">
          Seats available: {availableSeats}
        </p>
      </CardContent>

      <div className="w-full md:w-fit flex-shrink-0 mt-4 md:mt-0">
        <Button variant="default" onClick={onBook} className="w-full">
          Book Now
        </Button>
      </div>
    </Card>
  );
}
