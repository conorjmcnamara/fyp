import { getEnvVar } from '../utils/getEnvVar';

export const API_BASE_URL: string = getEnvVar('REACT_APP_BACKEND_URL');
export const MAX_TEXT_LENGTH: number = 1500;
export const MAX_FILE_SIZE_BYTES: number = 5 * 1024 * 1024;
export const PAPERS_PER_PAGE: number = 10;