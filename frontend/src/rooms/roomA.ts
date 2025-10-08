import { CinemaRoomSeat } from "@/models/cinema-room-seat.model"

export type RoomAType = [
    Array<
         CinemaRoomSeat[]
        >,
    Array<
         CinemaRoomSeat[]
        >
    ,
        Array<
         CinemaRoomSeat[]
        >
    ,
]

export const roomA: RoomAType = [
    Array(10).fill(null).map(() => (
        Array(4).fill(null).map((_, index) => ({ id: index + 1, seat_number: index + 1, status: 1 }))
    )),
    Array(10).fill(null).map(() => (
        Array(6).fill(null).map((_, index) => ({ id: index + 5, seat_number: index + 5, status: 1 }))
    )),
    Array(10).fill(null).map(() => (
         Array(4).fill(null).map((_, index) => ({ id: index + 11, seat_number: index + 11, status: 1 }))
    )),
]