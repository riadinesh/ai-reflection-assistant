// Base URL for the backend API.
// Set VITE_API_URL in production (e.g. your Render backend URL); falls back to
// the local dev server when unset.
export const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'
