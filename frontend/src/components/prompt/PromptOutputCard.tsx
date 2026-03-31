import { motion } from "framer-motion";
import MarkdownRenderer from "./MarkdownRenderer";
import CopyButton from "./CopyButton";

export default function PromptOutputCard({ text }: { text: string }) {
  return (
    <motion.div
      className="glass p-5 mt-6 relative"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <div className="absolute top-3 right-3">
        <CopyButton text={text} />
      </div>

      <MarkdownRenderer content={text} />
    </motion.div>
  );
}
