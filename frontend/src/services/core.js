import apiClient from "../api/apiClient";

export const getcore = async () => {
  const response = await apiClient.get("/api/yusuff");
  return response.data;
};
