import '@testing-library/jest-dom';

process.env.REACT_APP_BACKEND_URL = 'https://example.com';

afterAll(() => {
  delete process.env.REACT_APP_BACKEND_URL;
});
