import { motion } from "framer-motion";

const mockHistory = [
  "Improve API documentation",
  "Write better prompts for debugging",
  "Optimize ML pipeline prompts",
];

export default function Sidebar({
  onSelect,
}: {
  onSelect: (text: string) => void;
}) {
  return (
    <div className="w-64 h-screen border-r border-white/10 p-4 hidden md:block">
      <h2 className="text-sm mb-4 text-gray-400">History</h2>

      <div className="space-y-2">
        {mockHistory.map((item, i) => (
          <motion.div
            key={i}
            onClick={() => onSelect(item)}
            className="p-2 rounded-md hover:bg-white/5 cursor-pointer text-sm"
            whileHover={{ x: 4 }}
          >
            {item}
          </motion.div>
        ))}
      </div>
    </div>
  );
}
