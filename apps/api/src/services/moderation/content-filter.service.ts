export interface ModerationResult {
  flagged: boolean;
  categories: Record<string, boolean>;
  score: number;
}

export async function moderateContent(text: string): Promise<ModerationResult> {
  // In production: call OpenAI moderation API or custom classifier
  return { flagged: false, categories: { hate: false, violence: false, sexual: false }, score: 0 };
}
