import { motion } from "framer-motion";

export default function GenerateButton({
  loading,
  onClick,
}: {
  loading: boolean;
  onClick: () => void;
}) {
  return (
    <motion.button
      onClick={onClick}
      disabled={loading}
      className="btn w-full mt-4"
      whileTap={{ scale: 0.97 }}
    >
      {loading ? "Generating..." : "Generate Prompt"}
    </motion.button>
  );
}
