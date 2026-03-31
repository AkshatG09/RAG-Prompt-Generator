const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "";

function camelToSnake(obj: any): any {
  if (Array.isArray(obj)) return obj.map(camelToSnake);
  if (obj !== null && typeof obj === "object") {
    return Object.fromEntries(
      Object.entries(obj).map(([k, v]) => [
        k.replace(/[A-Z]/g, (l) => `_${l.toLowerCase()}`),
        camelToSnake(v),
      ]),
    );
  }
  return obj;
}

function snakeToCamel(obj: any): any {
  if (Array.isArray(obj)) return obj.map(snakeToCamel);
  if (obj !== null && typeof obj === "object") {
    return Object.fromEntries(
      Object.entries(obj).map(([k, v]) => [
        k.replace(/_([a-z])/g, (_, l) => l.toUpperCase()),
        snakeToCamel(v),
      ]),
    );
  }
  return obj;
}

export async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {},
): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${endpoint}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "API Error");
  }

  const data = await res.json();
  return snakeToCamel(data);
}

export async function postApi<T>(endpoint: string, body: any): Promise<T> {
  return fetchApi<T>(endpoint, {
    method: "POST",
    body: JSON.stringify(camelToSnake(body)),
  });
}
