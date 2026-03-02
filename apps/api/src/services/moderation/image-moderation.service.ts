export async function moderateImage(imageUrl: string): Promise<{ safe: boolean; reason?: string }> {
  // In production: call AWS Rekognition or Google Vision SafeSearch
  return { safe: true };
}
