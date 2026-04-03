export interface PromptGenerationRequest {
  userId: string;
  specialization: string;
  requestDescription: string;
}

export interface PromptGenerationResponse {
  generatedPrompt: string;
  retrievedContextUsed: string[] | null;
}

export interface HistoryEntry {
  id: string;
  userId: string;
  userRequest: string;
  generatedPrompt: string;
  retrievedContext: string[];
  timestamp: string;
}

export interface HistoryResponse {
  history: HistoryEntry[];
  totalCount: number;
}
