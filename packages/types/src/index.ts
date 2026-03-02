// Re-export all shared types + additional platform-specific ones
export * from "@cleus/shared";

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  pageSize: number;
  hasMore: boolean;
}

export interface WebSocketEvent<T = unknown> {
  type: string;
  payload: T;
  timestamp: string;
}

export interface GenerationJob {
  id: string;
  type: "image" | "video" | "story";
  status: "pending" | "processing" | "completed" | "failed";
  progress?: number;
  result?: string;
  error?: string;
  createdAt: string;
  updatedAt: string;
}

export interface CreditTransaction {
  id: string;
  userId: string;
  amount: number;
  type: "debit" | "credit";
  reason: string;
  createdAt: string;
}
