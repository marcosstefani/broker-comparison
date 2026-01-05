export const MESSAGE_COUNT = parseInt(process.env.MESSAGE_COUNT || "10000");
export const TOPIC_NAME = process.env.TOPIC_NAME || "benchmark_test";
export const PAYLOAD = { data: "x".repeat(100) };
