import { postApi } from "./apiClient";
import type { PromptGenerationRequest, PromptGenerationResponse } from "./types";

export function generatePrompt(
  data: PromptGenerationRequest,
): Promise<PromptGenerationResponse> {
  return postApi("/api/generate", data);
}
