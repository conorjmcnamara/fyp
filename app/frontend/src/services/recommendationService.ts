import { api } from '../utils/api';
import config from '../config/config';

export interface AuthorResponse {
  first_name: string;
  last_name: string;
}

export interface PaperResponse {
  id: string;
  title: string;
  year: number;
  abstract: string;
  venue: string;
  authors: AuthorResponse[];
  recommendation_score: number;
}

export interface RecommendationResponse {
  papers: PaperResponse[];
}

export const fetchRecommendations = async (
  title: string,
  abstract: string
): Promise<RecommendationResponse> => {
  const response = await api<RecommendationResponse>(config.apiBaseUrl, 'api/v1/recommendations', {
    method: 'POST',
    body: JSON.stringify({ title, abstract }),
    headers: {
      'Content-Type': 'application/json',
    },
  });
  
  return response;
};
