import { apiClient } from "../api/client";

export interface TokenResponse {
    access_token: string;
    token_type: string;
}

export const authApi = {
    /**
     * Register a new user. Returns { access_token, token_type }.
     */
    signup: (data: { email: string; password: string; name: string }) =>
        apiClient.post<TokenResponse>("/auth/signup", data),

    /**
     * Login. Backend expects form-data (OAuth2PasswordRequestForm).
     * Returns { access_token, token_type }.
     */
    login: (email: string, password: string) => {
        const form = new URLSearchParams();
        form.append("username", email); // OAuth2 spec uses "username" field
        form.append("password", password);
        return apiClient.post<TokenResponse>("/auth/login", form, {
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
        });
    },

    /** Logout — blacklists the token on the server. */
    logout: () => apiClient.post("/auth/logout"),

    /** Get current authenticated user info. */
    me: () => apiClient.get<{ id: number; email: string }>("/auth/me"),

    /** Request a password-reset email. */
    requestPasswordReset: (email: string) =>
        apiClient.post("/auth/request-password-reset", { email }),

    /** Complete a password reset with the token from email. */
    resetPassword: (token: string, new_password: string) =>
        apiClient.post("/auth/reset-password", { token, new_password }),
};
