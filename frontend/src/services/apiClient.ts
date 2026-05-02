// Architecture: React Frontend -> Node.js API Gateway -> Python Service
// This client establishes the bridge by centralizing all Gateway requests.

const GATEWAY_URL = process.env.NEXT_PUBLIC_GATEWAY_URL || 'http://localhost:3000/api';

/**
 * Creates an authorized request to the Node.js API Gateway, which
 * will then proxy internally to the Python services using microservice URLs.
 * 
 * @param endpoint - The API Gateway endpoint (e.g. '/ml/predict-risk')
 * @param method - 'GET', 'POST', 'PUT', 'DELETE'
 * @param body - Optional JSON body
 * @param getToken - Clerk's `getToken()` function from useAuth() hook
 */
export const fetchFromGateway = async (
  endpoint: string,
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' = 'GET',
  body?: any,
  getToken?: () => Promise<string | null>
) => {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  // If connected to Clerk auth, inject the Bearer token
  if (getToken) {
    const token = await getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
  }

  const options: RequestInit = {
    method,
    headers,
  };

  if (body) {
    options.body = JSON.stringify(body);
  }

  try {
    const response = await fetch(`${GATEWAY_URL}${endpoint}`, options);
    
    // Parse JSON
    const data = await response.json().catch(() => null);

    if (!response.ok) {
      throw new Error(data?.message || data?.error || `Gateway Error: ${response.status}`);
    }

    return data;
  } catch (error: any) {
    console.error(`[API Gateway Bridge Error] :: ${endpoint}`, error.message);
    throw error;
  }
};
