import { City } from "@/models/city.model";

export interface Cinema {
  id?: number;
  name?: string | null;
  city: City["id"];
  postal_code: string;
  street: string;
  street_number: string;
  url: string;
}
