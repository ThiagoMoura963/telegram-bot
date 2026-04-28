const PRODUCTION_API = "https://telegram-bot-backend-dpui.onrender.com";
const DEVELOPMENT_API = "http://localhost:8000";

const customApi = localStorage.getItem("API_URL");

export const API_URL =
  customApi ||
  (location.hostname.includes("localhost") ? DEVELOPMENT_API : PRODUCTION_API);
