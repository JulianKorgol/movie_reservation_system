import Skeleton from "react-loading-skeleton";
import "react-loading-skeleton/dist/skeleton.css";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
} from "@/components/ui/card";

const MovieCardSkeleton = () => (
  <Card className="overflow-hidden flex flex-col animate-pulse">
    <Skeleton height={192} width="100%" />
    <CardHeader>
      <Skeleton height={20} width="70%" />
      <Skeleton height={16} width="40%" />
    </CardHeader>
    <CardContent>
      <Skeleton count={2} />
    </CardContent>
    <CardFooter>
      <Skeleton height={32} width="100%" className="rounded" />
    </CardFooter>
  </Card>
);

export default MovieCardSkeleton;
