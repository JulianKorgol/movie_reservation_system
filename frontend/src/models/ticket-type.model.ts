import { Country } from "@/models/country.model";

export interface TicketType {
  id?: number;
  country?: Country["id"] | null;
  name: string;
  price: number | null;
  currency: string;
  primary_ticket?: TicketType["id"] | null;
  discount_percentage?: number | null;
}
