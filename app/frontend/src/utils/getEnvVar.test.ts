import { getEnvVar } from './getEnvVar';

describe('getEnvVar', () => {
  const originalEnv = process.env;

  beforeEach(() => {
    process.env = { ...originalEnv };
  });

  afterEach(() => {
    process.env = originalEnv;
  });

  it('should return the value of an existing environment variable', () => {
    process.env.TEST_VAR = 'test_value';

    const result = getEnvVar('TEST_VAR');

    expect(result).toBe('test_value');
  });

  it('should throw an error when the environment variable is missing', () => {
    expect(() => getEnvVar('MISSING_VAR')).toThrowError('Environment variable MISSING_VAR is missing');
  });

  it('should throw an error if the environment variable is empty', () => {
    process.env.EMPTY_VAR = '';

    expect(() => getEnvVar('EMPTY_VAR')).toThrowError('Environment variable EMPTY_VAR is missing');
  });
});
