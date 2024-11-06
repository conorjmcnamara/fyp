import { fetchApi } from "./api";
import { BACKEND_URL } from "../config";

interface MessageResponse {
    message: string;
}

export const fetchMessage = (): Promise<MessageResponse> => {
    return fetchApi<MessageResponse>(`${BACKEND_URL}/api/v1/message`);
};
