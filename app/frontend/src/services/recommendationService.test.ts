import { fetchRecommendations, RecommendationResponse } from './recommendationService';
import config from '../config/config';

global.fetch = jest.fn();

describe('fetchRecommendations', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should fetch recommendations successfully', async () => {
    const mockResponse: RecommendationResponse = {
      papers: [
        {
          id: '1',
          title: 'Paper 1',
          year: 2025,
          abstract: 'Abstract for paper 1',
          venue: 'Venue 1',
          authors: [{ first_name: 'John', last_name: 'Doe' }],
          recommendation_score: 95
        },
      ],
    };

    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse
    });

    const result = await fetchRecommendations('Example title', 'Example abstract', 10);

    expect(result).toEqual(mockResponse);
    expect(fetch).toHaveBeenCalledWith(`${config.apiBaseUrl}/api/v1/recommendations`, {
      method: 'POST',
      body: JSON.stringify(
        {
          title: 'Example title',
          abstract: 'Example abstract',
          numRecommendations: 10
        }
      ),
      headers: {
        'Content-Type': 'application/json',
      },
    });
  });

  it('should throw an error if the response is not OK', async () => {
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      status: 500,
      statusText: 'Internal Server Error'
    });

    await expect(fetchRecommendations('Example title', 'Example abstract', 10)).rejects.toThrow(
      'Request failed with status 500'
    );
  });

  it('should throw an error if the response is not valid JSON', async () => {
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => {
        throw new Error('Invalid JSON');
      }
    });

    await expect(fetchRecommendations('Example title', 'Example abstract', 10)).rejects.toThrow(
      'Invalid JSON'
    );
  });

  it('should throw an error if fetch fails due to network issues', async () => {
    (fetch as jest.Mock).mockRejectedValueOnce(new Error('Network Error'));

    await expect(fetchRecommendations('Example title', 'Example abstract', 10)).rejects.toThrow(
      'Network Error'
    );
  });
});
