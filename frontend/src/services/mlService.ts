import { fetchFromGateway } from './apiClient';

/**
 * Service to connect to the Machine Learning endpoints on the API Gateway.
 * Architecture Flow: Next.js -> Gateway (Express) -> Python ML Model
 */
export const MLService = {
  /**
   * Request a student dropout risk prediction.
   * Gateway passes this to `http://dropout-model:8001/predict`
   */
  async predictDropoutRisk(
    getToken: () => Promise<string | null>,
    features?: {
      attendance_rate?: number;
      test_scores?: number[];
      engagement_time?: number;
      assignment_completion?: number;
    }
  ) {
    return fetchFromGateway('/ml/predict-risk', 'POST', features, getToken);
  }
};
