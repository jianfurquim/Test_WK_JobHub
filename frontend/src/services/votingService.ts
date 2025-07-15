
import { apiRequest } from './api';

export const getTopics = async () => {
  return await apiRequest('/topics');
};

export const getTopicById = async (topicId: string) => {
  return await apiRequest(`/topics/${topicId}`);
};

export const openSession = async (topicId: string, duration?: number) => {
  const body = duration ? { duration } : {};
  return await apiRequest(`/topics/${topicId}/session`, {
    method: 'POST',
    body: JSON.stringify(body),
  });
};

export const vote = async (topicId: string, voto: 'SIM' | 'NAO') => {
  return await apiRequest(`/topics/${topicId}/vote`, {
    method: 'POST',
    body: JSON.stringify({ voto }),
  });
};

export const getResult = async (topicId: string) => {
  return await apiRequest(`/topics/${topicId}/result`);
};

export const createTopic = async (title: string, description: string) => {
  return await apiRequest('/topics', {
    method: 'POST',
    body: JSON.stringify({ title, description }),
  });
};
