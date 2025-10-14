'use client';

import { useEffect, useState } from 'react';

import { mockMovies } from '@/mocks/movies';
import { MovieGenre } from '@/models/movie-genre.model';
import { Movie } from '@/models/movie.model';
import Skeleton from 'react-loading-skeleton';
import 'react-loading-skeleton/dist/skeleton.css';

import Filters from '../components/Filters';
import MovieCard from '../components/MovieCard';
import MovieCardSkeleton from '../components/MovieCardSkeleton';
import SearchBar from '../components/SearchBar';

export default function HomePage() {
  const [movies, setMovies] = useState<Movie[]>([]);
  const [genres, setGenres] = useState<MovieGenre[]>([]);
  const [isLoadingMovies, setIsLoadingMovies] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedGenres, setSelectedGenres] = useState<string[]>([]);

  const api = process.env.NEXT_PUBLIC_API_URL;

  useEffect(() => {
    const fetchMovies = async () => {
      try {
        const today = new Date();
        today.setDate(today.getDate() + 1);
        const tomorrow = today.toISOString().split('T')[0];

        const response = await fetch(
          `${api}/reservation/showtimes?cinema_url=zlote-tarasy&date=${tomorrow}`
        );
        if (!response.ok) throw new Error('Failed to fetch movies');

        const data = await response.json();

        const formattedMovies: Movie[] = data.data.map((item: any) => {
          const mockMatch = mockMovies.find((mock) => mock.url === item.movie.url);

          return {
            title: item.movie.title,
            description: item.movie.description,
            genre: item.movie.genre
              ? {
                  name: item.movie.genre.name,
                  url: item.movie.genre.url,
                }
              : null,
            image_path: mockMatch?.image_path,
            url: item.movie.url,
          };
        });

        const uniqueGenres: MovieGenre[] = Array.from(
          new Map(
            formattedMovies
              .filter((movie) => movie.genre)
              .map((movie) => [movie.genre!.url, movie.genre!])
          ).values()
        );

        setMovies(formattedMovies);
        setGenres(uniqueGenres);
      } catch (error) {
        console.error('Error fetching movies:', error);
        setMovies([]);
        setGenres([]);
      } finally {
        setIsLoadingMovies(false);
      }
    };

    fetchMovies();
  }, [api]);

  const filteredMovies = movies.filter((movie) => {
    if (movie.genre?.url === 'none') return false;
    const matchesGenre =
      selectedGenres.length > 0 ? selectedGenres.includes(movie.genre?.name || '') : true;
    const matchesSearch = movie.title.toLowerCase().includes(searchQuery.toLowerCase());
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

      <Filters genres={genres} selectedGenres={selectedGenres} onFilterChange={setSelectedGenres} />

      <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-6">
        {isLoadingMovies
          ? Array.from({ length: 8 }).map((_, i) => <MovieCardSkeleton key={i} />)
          : filteredMovies.map((movie) => <MovieCard key={movie.url} movie={movie} />)}
      </div>
    </div>
  );
}
