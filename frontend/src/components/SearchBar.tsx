import { Input } from "@/components/ui/input";

interface SearchBarProps {
  query: string;
  onQueryChange: (query: string) => void;
}

const SearchBar = ({ query, onQueryChange }: SearchBarProps) => (
  <Input
    type="text"
    value={query}
    onChange={(e) => onQueryChange(e.target.value)}
    placeholder="Search movies..."
    className="w-full mt-2"
  />
);

export default SearchBar;
