import { TicketType } from "@/models/ticket-type.model";

export const mockTicketTypes: TicketType[] = [
  { id: 1, country: 1, name: "normal", price: 30, currency: "PLN" },
  { id: 2, country: 1, name: "discounted", price: null, currency: "PLN", primary_ticket: 1, discount_percentage: 20 },
  { id: 3, country: 1, name: "VIP", price: 40, currency: "PLN", primary_ticket: 1 },
  { id: 4, country: 2, name: "normal", price: 8, currency: "EUR" },
  { id: 5, country: 2, name: "discounted", price: null, currency: "EUR", primary_ticket: 4, discount_percentage: 15 },
  { id: 6, country: 2, name: "VIP", price: 12, currency: "EUR", primary_ticket: 4 },
  { id: 7, country: 3, name: "normal", price: 10, currency: "EUR" },
  { id: 8, country: 3, name: "discounted", price: null, currency: "EUR", primary_ticket: 7, discount_percentage: 10 },
  { id: 9, country: 3, name: "VIP", price: 15, currency: "EUR", primary_ticket: 7 },
  { id: 10, country: 4, name: "normal", price: 9, currency: "EUR" },
  { id: 11, country: 4, name: "discounted", price: null, currency: "EUR", primary_ticket: 10, discount_percentage: 5 },
  { id: 12, country: 4, name: "VIP", price: 14, currency: "EUR", primary_ticket: 10 },
];
