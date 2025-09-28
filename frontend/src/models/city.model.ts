import { Country } from "@/models/country.model";

export interface City {
  id?: string;
  name: string;
  country: Country;
  url: string;
}
