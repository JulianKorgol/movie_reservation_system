import Skeleton from "react-loading-skeleton";
import "react-loading-skeleton/dist/skeleton.css";

export default function MovieDetailsSkeleton() {
  return (
    <div className="p-6 max-w-7xl mx-auto flex flex-col md:flex-row gap-6 animate-pulse">
      {/* Poster Skeleton */}
      <div className="md:w-1/2 w-full h-[400px]">
        <Skeleton className="h-full w-full rounded-md" />
      </div>

      {/* Text Skeleton */}
      <div className="flex flex-col justify-between md:w-1/2 gap-4">
        {/* Title */}
        <Skeleton height={32} width="60%" />
        {/* Genre */}
        <Skeleton height={20} width="40%" />
        {/* Description */}
        <Skeleton count={4} />
        {/* Button */}
        <Skeleton height={40} width="50%" className="mt-4 rounded" />
      </div>
    </div>
  );
}
