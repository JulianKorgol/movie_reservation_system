import { roomA, RoomAType } from "@/rooms/roomA";
import Seat from "./ui/seat";
import { RoomBType } from "@/rooms/roomB";

export default function Room({ room }: { room: RoomAType | RoomBType }) {
  return (
    <div className="flex-1 flex gap-2">
      <div className="flex flex-col gap-2.5">
        {room[0].map((_, index) => {
          return (
            <span className="text-sm text-gray-500 h-7 items-center flex" key={index}>
              {index}
            </span>
          );
        })}
      </div>
      <div className="flex flex-1 justify-between">
        {room.map((column, columnNr) => {
          return (
            <div key={columnNr} className="flex flex-col gap-2">
              {column.map((row, index) => {
                return (
                  <div key={index} className="flex gap-1 items-center">
                    {row.map((seat) => (
                      <Seat
                        key={seat.id}
                        status={seat.status === 1 ? "available" : "unavailable"}
                        number={seat.seat_number}
                      />
                    ))}
                  </div>
                );
              })}
            </div>
          );
        })}
      </div>
    </div>
  );
}
