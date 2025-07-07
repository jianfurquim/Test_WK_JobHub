
import { apiRequest } from './api';

export const login = async (credentials: { cpf: string; senha: string }) => {
  return await apiRequest('/login', {
    method: 'POST',
    body: JSON.stringify(credentials),
  });
};

export const register = async (userData: { nome: string; cpf: string; senha: string }) => {
  return await apiRequest('/register', {
    method: 'POST',
    body: JSON.stringify(userData),
  });
};
