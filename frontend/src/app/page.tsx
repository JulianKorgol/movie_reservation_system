'use client';

import { useEffect, useState } from 'react';

import { mockGenres } from '@/mocks/genres';
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
        // get tomorrow’s date in YYYY-MM-DD
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        const formattedDate = tomorrow.toISOString().split('T')[0];

        const response = await fetch(
          `${api}/reservation/showtimes?cinema_url=zlote-tarasy&date=${formattedDate}`
        );
        if (!response.ok) throw new Error('Failed to fetch movies');

        const json = await response.json();
        console.log('API response:', json.data);

        // Extract data.data from response
        const formattedMovies: Movie[] = json.data.map((item: any) => ({
          title: item.movie.title,
          description: item.movie.description,
          genre: { name: item.movie.genre_url },
          image_path: 'https://image.tmdb.org/t/p/w1280/9PXZIUsSDh4alB80jheWX4fhZmy.jpg',
          url: item.movie.url,
          showtimes: item.showtimes || [],
        }));

        setMovies(formattedMovies);
        setGenres(mockGenres); // temporary until real genres come from API
      } catch (error) {
        console.error('Error fetching movies:', error);
        setMovies(mockMovies);
        setGenres(mockGenres);
      } finally {
        setIsLoadingMovies(false);
      }
    };

    fetchMovies();
  }, [api]);

  const filteredMovies = movies.filter((movie) => {
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
          : filteredMovies.map((movie, i) => (
              <MovieCard key={movie.url || `${movie.title}-${i}`} movie={movie} />
            ))}
      </div>
    </div>
  );
}
