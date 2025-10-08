import "@/styles/seat.scss";
import { Icon } from "@iconify/react/dist/iconify.js";

export default function Seat({ status, number }: { status: "available" | "selected" | "unavailable"; number: number }) {
  return (
    <div className="flex flex-col gap-0.5 items-center cursor-pointer transition-all">
      <div className={`w-7 h-6 flex justify-center items-center rounded-t-md rounded-b-sm text-black seat-${status}`}>
        {status === "unavailable" ? (
          <Icon icon={"material-symbols:close-small-rounded"} className="text-xl" />
        ) : (
          <span className="text-sm">{number}</span>
        )}
      </div>
      <span className={`w-6 h-1 rounded-sm seat-${status}`} />
    </div>
  );
}
