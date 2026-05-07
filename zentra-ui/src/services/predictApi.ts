import { apiClient } from "../api/client";

export const predictApi = {
    // Backend reads the profile from DB — no body needed
    run: () =>
        apiClient.post<{ obesity_level: string }>("/predict/"),
};
