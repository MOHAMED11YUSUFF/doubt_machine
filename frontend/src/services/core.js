import apiClient from "../api/apiClient";

export const getcore = async () => {
  const response = await apiClient.get("/api/yusuff");
  return response.data;
};

export const loginUser = async (email, password) => {
  try {
    const response = await apiClient.post("/admin/auth/login/", { email, password });
    return response.data;
  } catch (error) {
    throw new Error("Authentication failed");
  }
};