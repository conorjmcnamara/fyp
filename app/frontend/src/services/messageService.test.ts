import { fetchMessage } from "./messageService";
import { api } from '../utils/api';
import config from '../config/config';

jest.mock('../utils/api');

describe('fetchMessage', () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  it('should call api with the correct endpoint and return the message response on success', async () => {
    const mockMessageResponse = { message: 'Hello' };

    (api as jest.Mock).mockResolvedValueOnce(mockMessageResponse);

    const result = await fetchMessage();

    expect(api).toHaveBeenCalledWith(config.apiBaseUrl, 'api/v1/message');
    expect(result).toEqual(mockMessageResponse);
  });

  it('should propagate errors thrown by api', async () => {
    const errorMessage = 'Error';

    (api as jest.Mock).mockRejectedValueOnce(new Error(errorMessage));

    await expect(fetchMessage()).rejects.toThrow(errorMessage);
  });
});
