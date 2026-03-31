import { useMutation } from "@tanstack/react-query";
import { generatePrompt } from "@/api/promptApi";

export function useGeneratePrompt() {
  return useMutation({
    mutationFn: generatePrompt,
  });
}
