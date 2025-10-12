import axios from 'axios';

const server = process.env.BACKEND_URL || 'http://localhost:8000';

const get = async (endpoint: string, params?: any, headers?: any, options?: any) => {
  return axios.get(`${server}/${endpoint}`, { params, headers, ...options });
};

const post = async (endpoint: string, data?: any, headers?: any, options?: any) => {
  return axios.post(`${server}/${endpoint}`, data, { headers, ...options });
};

export default {
  get,
  post,
};
