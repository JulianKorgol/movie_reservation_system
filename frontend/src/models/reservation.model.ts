import { Account } from "@/models/account.model";
import { Showtime } from "@/models/showtime.model";

export interface Reservation {
  id?: string;
  account?: Account | null;
  showtime?: Showtime | null;
  status: 1 | 2 | 3; // 1 - confirmed, 2 - cancelled, 3 - in progress
  token?: string | null;
  first_name?: string | null;
  last_name?: string | null;
  email?: string | null;
  payment_status: 1 | 2 | 3 | 4; // 1 - paid, 2 - unpaid, 3 - does not require payment, 4 - refunded
  payment_stripe_id?: string | null;
  created_at: string;
}
