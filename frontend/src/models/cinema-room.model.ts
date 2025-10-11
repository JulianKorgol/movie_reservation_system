import { Cinema } from "@/models/cinema.model";

export interface CinemaRoom {
  id?: number;
  name: string;
  status: 0 | 1; // 0 - broken, 1 - working
  cinema: Cinema["id"];
  type: "A" | "B" | "C"; // A - 3 columns, B - 2 columns, C - 1 column
}
