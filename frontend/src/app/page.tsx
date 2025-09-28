"use client";

import { useState, useEffect } from "react";
import Skeleton from "react-loading-skeleton";
import "react-loading-skeleton/dist/skeleton.css";

import { Movie } from "@/models/movie.model";
import { MovieGenre } from "@/models/movie-genre.model";

import MovieCard from "../components/MovieCard";
import MovieCardSkeleton from "../components/MovieCardSkeleton";
import Filters from "../components/Filters";
import SearchBar from "../components/SearchBar";

import { mockMovies } from "@/mocks/movies";
import { mockGenres } from "@/mocks/genres";

export default function HomePage() {
  const [movies, setMovies] = useState<Movie[]>([]);
  const [genres, setGenres] = useState<MovieGenre[]>([]);
  const [isLoadingMovies, setIsLoadingMovies] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedGenres, setSelectedGenres] = useState<string[]>([]);

  useEffect(() => {
    setTimeout(() => {
      setMovies(mockMovies);
      setGenres(mockGenres);
      setIsLoadingMovies(false);
    }, 1000);
  }, []);

  const filteredMovies = movies.filter((movie) => {
    const matchesGenre =
      selectedGenres.length > 0
        ? selectedGenres.includes(movie.genre?.name || "")
        : true;
    const matchesSearch = movie.title
      .toLowerCase()
      .includes(searchQuery.toLowerCase());
    return matchesGenre && matchesSearch;
  });

  return (
    <div className="p-6 max-w-7xl mx-auto pt-32">
      <h1 className="text-3xl font-bold mb-4">Movie Listings</h1>
      {isLoadingMovies ? (
        <Skeleton height={40} className="rounded-lg mt-2" />
      ) : (
        <SearchBar query={searchQuery} onQueryChange={setSearchQuery} />
      )}

      <Filters
        genres={genres}
        selectedGenres={selectedGenres}
        onFilterChange={setSelectedGenres}
      />

      <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-6">
        {isLoadingMovies
          ? Array.from({ length: 8 }).map((_, i) => (
              <MovieCardSkeleton key={i} />
            ))
          : filteredMovies.map((movie) => (
              <MovieCard key={movie.id} movie={movie} />
            ))}
      </div>
    </div>
  );
}
