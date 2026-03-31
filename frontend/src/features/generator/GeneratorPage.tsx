import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { toast } from "sonner";
import { useGeneratePrompt } from "@/hooks/useGeneratePrompt";
import { useUserStore } from "@/stores/useUserStore";
import PromptInputCard from "@/components/prompt/PromptInputCard";
import GenerateButton from "@/components/prompt/GenerateButton";
import TemplateGrid from "@/components/prompt/TemplateGrid";
import PromptOutputCard from "@/components/prompt/PromptOutputCard";

export default function GeneratorPage() {
  const { userId, specialization } = useUserStore();
  const [request, setRequest] = useState("");

  const mutation = useGeneratePrompt();

  const handleGenerate = () => {
    mutation.mutate(
      {
        userId,
        specialization,
        requestDescription: request,
      },
      {
        onSuccess: () => toast.success("Prompt generated!"),
        onError: () => toast.error("Generation failed"),
      }
    );
  };

  return (
    <div>
      <motion.h1
        className="text-3xl font-semibold mb-6"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        AI Prompt Generator
      </motion.h1>

      <TemplateGrid onSelect={(text) => setRequest(text)} />

      <PromptInputCard value={request} onChange={setRequest} />

      <GenerateButton loading={mutation.isPending} onClick={handleGenerate} />

      <AnimatePresence>
        {mutation.data && (
          <motion.div
            key="output"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <PromptOutputCard text={mutation.data.generatedPrompt} />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
