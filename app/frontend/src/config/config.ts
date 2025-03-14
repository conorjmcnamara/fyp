import { getEnvVar } from '../utils/getEnvVar';

export const MAX_TEXT_LENGTH: number = 1500;
export const API_BASE_URL: string = getEnvVar('REACT_APP_BACKEND_URL');
