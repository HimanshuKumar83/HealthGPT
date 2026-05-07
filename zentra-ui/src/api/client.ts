import axios from "axios";

// ─── Base URL ────────────────────────────────────────────────────────────────
// In dev, Vite proxy forwards /api → http://127.0.0.1:8000
// In production, set VITE_API_BASE_URL to your Railway backend URL
const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "https://zentra-backend-umdc.onrender.com";

// ─── Axios Instance ───────────────────────────────────────────────────────────
export const apiClient = axios.create({
    baseURL: BASE_URL,
    headers: {
        "Content-Type": "application/json",
    },
    withCredentials: false,
});

// ─── Request Interceptor — attach Bearer token ────────────────────────────────
apiClient.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("access_token");
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// ─── Response Interceptor — handle 401 (token expired / invalid) ─────────────
apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Clear stored token and redirect to login
            localStorage.removeItem("access_token");
            localStorage.removeItem("user");
            window.location.href = "/login";
        }
        return Promise.reject(error);
    }
);
