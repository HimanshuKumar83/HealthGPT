import axios from "axios";

// ─── Base URL ────────────────────────────────────────────────────────────────
// VITE_API_URL is used by the local setup; VITE_API_BASE_URL remains supported
// for existing production deployments.
const BASE_URL =
    import.meta.env.VITE_API_URL ??
    import.meta.env.VITE_API_BASE_URL ??
    "http://127.0.0.1:8000";

// ─── Axios Instance ───────────────────────────────────────────────────────────
export const apiClient = axios.create({
    baseURL: BASE_URL,
    timeout: 15000,
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
        const isAuthRoute =
            window.location.pathname === "/login" ||
            window.location.pathname === "/register";
        if (error.response?.status === 401 && !isAuthRoute) {
            // Clear stored token and redirect to login
            localStorage.removeItem("access_token");
            localStorage.removeItem("user");
            window.location.href = "/login";
        }
        return Promise.reject(error);
    }
);
