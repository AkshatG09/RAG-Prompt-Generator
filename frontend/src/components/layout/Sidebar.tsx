import { motion } from "framer-motion";
import { useHistory } from "@/hooks/useHistory";
import { useUserStore } from "@/stores/useUserStore";

export default function Sidebar({
  onSelect,
}: {
  onSelect: (text: string) => void;
}) {
  const { userId } = useUserStore();
  const { data, isLoading, isError } = useHistory(userId);

  return (
    <div className="w-64 h-screen border-r border-white/10 p-4 hidden md:block">
      <h2 className="text-sm mb-4 text-gray-400">History</h2>

      <div className="space-y-2">
        {isLoading && (
          <p className="text-sm text-gray-500">Loading...</p>
        )}

        {isError && (
          <p className="text-sm text-red-400">Failed to load history</p>
        )}

        {!isLoading && !isError && (!data?.history || data.history.length === 0) && (
          <p className="text-sm text-gray-500">No history yet</p>
        )}

        {data?.history.map((entry) => (
          <motion.div
            key={entry.id}
            onClick={() => onSelect(entry.userRequest)}
            className="p-2 rounded-md hover:bg-white/5 cursor-pointer text-sm truncate"
            whileHover={{ x: 4 }}
          >
            {entry.userRequest}
          </motion.div>
        ))}
      </div>
    </div>
  );
}
