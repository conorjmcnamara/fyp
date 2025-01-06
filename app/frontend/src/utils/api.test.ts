import { api } from './api';

global.fetch = jest.fn();

describe('api', () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  it('should return parsed JSON data on a successful response', async () => {
    const mockResponse = { data: 'Data' };
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse
    });

    const result = await api('https://example.com', 'endpoint');
    
    expect(result).toEqual(mockResponse);
    expect(fetch).toHaveBeenCalledWith('https://example.com/endpoint', {});
  });

  it('should throw an error with the error message on a failed response', async () => {
    const errorResponse = { error: 'Not found' };
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      status: 404,
      json: async () => errorResponse
    });

    await expect(api('https://example.com', 'nonexistent-endpoint')).rejects.toThrow('Not found');
  });

  it('should throw a default error message when the response does not include an error message', async () => {
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      status: 500,
      json: async () => ({})
    });

    await expect(api('https://example.com', 'error-endpoint')).rejects.toThrow('Error: 500');
  });

  it('should handle request options', async () => {
    const mockResponse = { data: 'Custom options' };
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse
    });
  
    const options = { method: 'POST', headers: { 'Content-Type': 'application/json' } };
    const result = await api('https://example.com', 'endpoint', options);
  
    expect(result).toEqual(mockResponse);
    expect(fetch).toHaveBeenCalledWith('https://example.com/endpoint', options);
  });
});
