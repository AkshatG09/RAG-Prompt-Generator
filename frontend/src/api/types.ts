export interface PromptGenerationRequest {
  userId: string;
  specialization: string;
  requestDescription: string;
}

export interface PromptGenerationResponse {
  generatedPrompt: string;
  retrievedContextUsed: string[] | null;
}
