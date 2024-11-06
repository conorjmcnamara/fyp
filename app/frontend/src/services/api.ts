export const fetchApi = async <T>(url: string, options?: RequestInit): Promise<T> => {
    const response = await fetch(url, options);

    if (!response.ok) {
        const errorBody = await response.json();
        const errorMessage = (errorBody && errorBody.error) || `Error: ${response.status}`;
        throw new Error(errorMessage);
    }

    const data: T = await response.json();
    return data;
};
