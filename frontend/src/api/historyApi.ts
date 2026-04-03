import { fetchApi } from "./apiClient";
import type { HistoryResponse } from "./types";

export function fetchHistory(
  userId: string,
  limit: number = 30,
  offset: number = 0,
): Promise<HistoryResponse> {
  return fetchApi(`/api/history/${userId}?limit=${limit}&offset=${offset}`);
}
