import { useEffect, useState } from "react";
import { getcore } from "../services/core";

function Page() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      const data = await getcore();
      setMessage(data.message);
    };

    fetchData();
  }, []);

  return (
    <div>
      <h2>FastAPI Response</h2>
      <p>{message}</p>
    </div>
  );
}

export default Page;