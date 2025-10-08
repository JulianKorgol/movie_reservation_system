import { CinemaRoomSeat } from "@/models/cinema-room-seat.model";

export type RoomBType = [Array<CinemaRoomSeat[]>, Array<CinemaRoomSeat[]>];

export const roomB: RoomBType = [
  Array(10)
    .fill(null)
    .map(() =>
      Array(8)
        .fill(null)
        .map((_, index) => ({ id: index + 1, seat_number: index + 1, status: 1 }))
    ),
  Array(10)
    .fill(null)
    .map(() =>
      Array(8)
        .fill(null)
        .map((_, index) => ({ id: index + 5, seat_number: index + 5, status: 1 }))
    ),
];
