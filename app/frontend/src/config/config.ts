import { getEnvVar } from '../utils/getEnvVar';

interface Config {
  apiBaseUrl: string;
}

const config: Config = {
  apiBaseUrl: getEnvVar('REACT_APP_BACKEND_URL')
};

export default config;
