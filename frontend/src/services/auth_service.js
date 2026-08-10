import axios from "axios";

const API = "http://localhost:5000/api/auth";

// MUST MATCH THIS NAME
export const loginUser = (data) => {
  return axios.post(`${API}/login`, data);
};

//  register
export const registerUser = (data) => {
  return axios.post(`${API}/register`, data);
};