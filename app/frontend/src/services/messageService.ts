import { api } from '../utils/api';
import config from '../config/config';

interface MessageResponse {
  message: string;
}

export const fetchMessage = async (): Promise<MessageResponse> => {
  return api<MessageResponse>(config.apiBaseUrl, 'api/v1/message');
};
