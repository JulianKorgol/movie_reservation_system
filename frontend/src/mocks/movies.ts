import { Movie } from "@/models/movie.model";
import { mockGenres } from "@/mocks/genres";

export const mockMovies: Movie[] = [
  {
    id: 1,
    title: "F1",
    description:
      "Racing legend Sonny Hayes is coaxed out of retirement to lead a struggling Formula 1 team—and mentor a young hotshot driver—while chasing one more chance at glory",
    genre: mockGenres[1],
    image_path: "https://image.tmdb.org/t/p/w1280/9PXZIUsSDh4alB80jheWX4fhZmy.jpg",
    url: "f1",
  },
  {
    id: 2,
    title: "The Fantastic 4: First Steps",
    description:
      "Against the vibrant backdrop of a 1960s-inspired, retro-futuristic world, Marvel's First Family is forced to balance their roles as heroes with the strength of their family bond, while defending Earth from a ravenous space god called Galactus and his enigmatic Herald, Silver Surfer",
    genre: mockGenres[0],
    image_path: "https://image.tmdb.org/t/p/w1280/cm8TNGBGG0aBfWj0LgrESHv8tir.jpg",
    url: "the-fantastic-4-first-steps",
  },
  {
    id: 3,
    title: "The Falcon and the Winter Soldier",
    description:
      "Following the events of “Avengers: Endgame”, the Falcon, Sam Wilson and the Winter Soldier, Bucky Barnes team up in a global adventure that tests their abilities, and their patience",
    genre: mockGenres[0],
    image_path: "https://image.tmdb.org/t/p/w1280/6kbAMLteGO8yyewYau6bJ683sw7.jpg",
    url: "the-marvels",
  },
  {
    id: 4,
    title: "John Wick: Chapter 4",
    description:
      "With the price on his head ever increasing, John Wick uncovers a path to defeating The High Table. But before he can earn his freedom, Wick must face off against a new enemy with powerful alliances across the globe and forces that turn old friends into foes",
    genre: mockGenres[1],
    image_path: "https://image.tmdb.org/t/p/w1280/vZloFAK7NmvMGKE7VkF5UHaz0I.jpg",
    url: "john-wick-chapter-4",
  },
];
