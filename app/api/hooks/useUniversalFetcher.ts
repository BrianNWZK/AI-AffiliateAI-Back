import { useCallback, useState } from "react";

export function useUniversalFetcher<T = any>() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<T | null>(null);

  const fetchUniversal = useCallback(async (target: string, opts?: RequestInit) => {
    setLoading(true);
    setError(null);
    setData(null);
    try {
      const res = await fetch(`/api/universal?target=${encodeURIComponent(target)}`, opts);
      if (!res.ok) throw new Error("API error");
      const json = await res.json();
      setData(json);
      return json;
    } catch (e: any) {
      setError(e.message);
      throw e;
    } finally {
      setLoading(false);
    }
  }, []);

  return { loading, error, data, fetchUniversal };
}
