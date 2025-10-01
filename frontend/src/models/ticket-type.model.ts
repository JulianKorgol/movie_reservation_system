import { Country } from '@/models/country.model';

export interface TicketType {
  id?: number;
  country?: Country | null;
  name: string;
  price: number;
  currency: string;
  primary_ticket?: TicketType | null;
  discount_percentage?: number | null;
}
