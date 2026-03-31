import { motion } from "framer-motion";

const templates = [
  {
    label: "Improve Writing",
    text: "Create a prompt to improve clarity of technical writing...",
  },
  {
    label: "Debug Code",
    text: "Generate a prompt to debug complex code issues...",
  },
  {
    label: "Summarization",
    text: "Create a prompt to summarize long documents...",
  },
];

export default function TemplateGrid({
  onSelect,
}: {
  onSelect: (text: string) => void;
}) {
  return (
    <div className="grid grid-cols-2 gap-3 mt-6">
      {templates.map((t) => (
        <motion.div
          key={t.label}
          onClick={() => onSelect(t.text)}
          className="glass p-4 cursor-pointer"
          whileHover={{ scale: 1.03 }}
        >
          <p className="text-sm font-medium">{t.label}</p>
        </motion.div>
      ))}
    </div>
  );
}
