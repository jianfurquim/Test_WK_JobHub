
import { apiRequest } from './api';

export const login = async (credentials: { cpf: string; password: string }) => {
  return await apiRequest('/login', {
    method: 'POST',
    body: JSON.stringify(credentials),
  });
};

export const register = async (userData: { name: string; cpf: string; password: string }) => {
  return await apiRequest('/register', {
    method: 'POST',
    body: JSON.stringify(userData),
  });
};
