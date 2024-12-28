"use client";
import { useState } from "react";
import axios from "axios";

interface ScrapeData {
  trends: string[];
  date_time_of_end: string;
  ip_address: string;
  _id: string;
}

export default function Home() {
  const [data, setData] = useState<ScrapeData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleScrape = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await axios.get("http://localhost:3001/api/scrape");
      setData(res.data);
    } catch (err) {
      setError("Failed to fetch data. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="pt-10 pl-4 text-black ">
      {error && <p className="text-red-500">{error}</p>}
      {data ? (
        <div>
          <p>
            These are the most happening topics as on{" "}
            <span className="font-bold">{data.date_time_of_end}</span>
          </p>
          <ul className="py-4">
            {data.trends?.map((trend, index) => (
              <li key={index}>- {trend}</li>
            ))}
          </ul>
          <p>
            The IP address used for this query was{" "}
            <span className="font-bold">{data.ip_address}</span>.
          </p>
          <p className="pt-2">
            Here’s a JSON extract of this record from the MongoDB:
          </p>
          <pre className="py-2">{JSON.stringify(data, null, 2)}</pre>
          <button
            disabled={loading}
            onClick={handleScrape}
            className="text-blue-600"
          >
            {loading ? "Loading..." : "Click here to run the query again."}
          </button>
        </div>
      ) : (
        <button
          disabled={loading}
          onClick={handleScrape}
          className="text-blue-600"
        >
          {loading ? "Loading..." : "Click here to run the script."}
        </button>
      )}
    </div>
  );
}
