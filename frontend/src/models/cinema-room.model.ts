import { Cinema } from '@/models/cinema.model';

export interface CinemaRoom {
  id?: number;
  name: string;
  status: 0 | 1; // 0 - broken, 1 - working
  cinema: Cinema;
}
