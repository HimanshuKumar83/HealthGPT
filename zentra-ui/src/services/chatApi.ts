import { apiClient } from "../api/client";

export interface ChatSessionSummary {
    id: string;
    title: string;
    created_at: string;
    updated_at: string;
    message_count: number;
}

export interface ChatMessage {
    id: number;
    role: "user" | "assistant";
    content: string;
    created_at: string;
}

export interface ChatSessionDetail {
    id: string;
    title: string;
    created_at: string;
    updated_at: string;
    messages: ChatMessage[];
}

export const chatApi = {
    listSessions: () =>
        apiClient.get<{ sessions: ChatSessionSummary[]; total: number }>("/chat/sessions"),

    createSession: () =>
        apiClient.post<ChatSessionSummary>("/chat/sessions"),

    getSession: (sessionId: string) =>
        apiClient.get<ChatSessionDetail>(`/chat/sessions/${sessionId}`),

    sendMessage: (sessionId: string, message: string) =>
        apiClient.post<{ message: ChatMessage; session_id: string }>(
            `/chat/sessions/${sessionId}/messages`,
            { message }
        ),

    renameSession: (sessionId: string, title: string) =>
        apiClient.patch<ChatSessionSummary>(`/chat/sessions/${sessionId}/title`, { title }),

    deleteSession: (sessionId: string) =>
        apiClient.delete(`/chat/sessions/${sessionId}`),

    streamMessage: async (sessionId: string, message: string, onChunk: (chunk: string) => void) => {
        const token = localStorage.getItem("access_token");
        const response = await fetch(`${apiClient.defaults.baseURL}/chat/sessions/${sessionId}/stream`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
            },
            body: JSON.stringify({ message }),
        });

        if (!response.ok) throw new Error("Failed to start stream");

        const reader = response.body?.getReader();
        const decoder = new TextDecoder();
        let buffer = "";

        if (!reader) return;

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split("\n\n");
            buffer = lines.pop() || "";

            for (const line of lines) {
                if (line.startsWith("data: ")) {
                    const data = line.slice(6);
                    if (data === "[DONE]") return;
                    try {
                        const { chunk } = JSON.parse(data);
                        if (chunk) onChunk(chunk);
                    } catch (e) {
                        console.error("Error parsing stream chunk", e);
                    }
                }
            }
        }
    },
};
