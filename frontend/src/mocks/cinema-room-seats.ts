import { CinemaRoomSeat } from "@/models/cinema-room-seat.model";
import { mockCinemaRoomRows } from "./cinema-room-rows";
import { mockCinemaRooms } from "./cinema-room";
import { mockCinemas } from "./cinemas";

const SEATS_IN_ROOM_TYPE = { A: 14, B: 12, C: 10 } as const; // Number of seats per row for each type
const SEAT_TYPE = { NORMAL: 1, VIP: 2 } as const; // 1 - NORMAL, 2 - VIP

const generatedSeats: CinemaRoomSeat[] = [];

mockCinemas.forEach((cinema) => {
  const roomsInCinema = mockCinemaRooms.filter((room) => room.cinema === cinema.id && room.status === 1);

  roomsInCinema.forEach((room) => {
    const rowsInRoom = mockCinemaRoomRows.filter((row) => row.cinema_room === room.id);
    const seatsPerRow = SEATS_IN_ROOM_TYPE[room.type as keyof typeof SEATS_IN_ROOM_TYPE];

    rowsInRoom.forEach((row, rowNumber) => {
      for (let seatNumber = 1; seatNumber <= seatsPerRow; seatNumber++) {
        generatedSeats.push({
          id: generatedSeats.length + 1,
          seat_number: seatNumber,
          row: row.id,
          status: 1, // All seats are working
          seat_type: rowNumber === 6 || rowNumber === 7 ? SEAT_TYPE.VIP : SEAT_TYPE.NORMAL, // rows 7 and 8 are VIP
        });
      }
    });
  });
});

export const mockCinemaRoomSeats: CinemaRoomSeat[] = generatedSeats;
