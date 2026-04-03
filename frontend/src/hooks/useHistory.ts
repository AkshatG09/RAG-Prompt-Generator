import { useQuery } from "@tanstack/react-query";
import { fetchHistory } from "@/api/historyApi";

export function useHistory(userId: string, limit?: number, offset?: number) {
  return useQuery({
    queryKey: ["history", userId, limit, offset],
    queryFn: () => fetchHistory(userId, limit, offset),
    enabled: !!userId,
  });
}
