export const api = async <T>(baseUrl: string, endpoint: string, options: RequestInit = {}): Promise<T> => {
  const response = await fetch(`${baseUrl}/${endpoint}`, options);

  if (!response.ok) {
    const errorBody = await response.json();
    const errorMessage = (errorBody && errorBody.error) || `Error: ${response.status}`;
    throw new Error(errorMessage);
  }

  return response.json();
};
