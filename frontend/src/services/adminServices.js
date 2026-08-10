import axios from "axios";

const API = "http://127.0.0.1:5000/api/admin";

// GET all staff
export const getStaff = () => {
  return axios.get(`${API}/staff`);
};

// CREATE staff
export const createStaffAPI = (data) => {
  return axios.post(`${API}/staff`, data);
};

// UPDATE status
export const updateStaffStatus = (id, status) => {
  return axios.put(`${API}/staff/${id}`, { status });
};