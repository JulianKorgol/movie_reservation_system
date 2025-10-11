import { Country } from "@/models/country.model";

export interface City {
  id?: number;
  name: string;
  country: Country["id"];
  url: string;
}
