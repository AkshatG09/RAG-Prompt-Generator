import { motion } from "framer-motion";

export default function PromptInputCard({
  value,
  onChange,
}: {
  value: string;
  onChange: (v: string) => void;
}) {
  return (
    <motion.div
      className="glass p-5"
      initial={{ opacity: 0, scale: 0.98 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
    >
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Describe what you want to generate..."
        className="w-full bg-transparent outline-none resize-none text-sm"
        rows={5}
      />
    </motion.div>
  );
}
