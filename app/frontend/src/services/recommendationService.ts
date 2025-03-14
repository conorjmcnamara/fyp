import { API_BASE_URL } from '../config/config';

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
  abstract: string,
  numRecommendations: number
): Promise<RecommendationResponse> => {
  const response = await fetch(`${API_BASE_URL}/api/v1/recommendations`, {
    method: 'POST',
    body: JSON.stringify({ title, abstract, numRecommendations }),
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }
  
  return response.json();
};

export const uploadPdf = async (
  file: File,
  numRecommendations: number
): Promise<{ papers: PaperResponse[] }> => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('numRecommendations', numRecommendations.toString()); 

  const response = await fetch(`${API_BASE_URL}/api/v1/recommendations/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }

  return response.json();
};
