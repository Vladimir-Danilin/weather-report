import axios from "axios";

const API_BASE_URL = "http://localhost:8000"; // поменяй на prod URL при деплое

const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 5000,
});

export default api;
