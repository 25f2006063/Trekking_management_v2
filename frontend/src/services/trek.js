import api from "./api";

export const getTreks = () => api.get("/user/treks");
export const bookTrek = (id) => api.post(`/user/book/${id}`);
export const getAdminTreks = () => api.get("/admin/treks");
export const createTrek = (data) => api.post("/admin/treks", data);