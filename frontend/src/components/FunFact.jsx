// eslint-disable-next-line no-unused-vars
import React, { useState, useEffect } from "react";
import "../styles/FunFact.css";

const FunFact = () => {
  const [message, setMessage] = useState("");

  useEffect(() => {
    const ws = new WebSocket(
      "ws://" +
        import.meta.env.VITE_API_URL.replace(/(^\w+:|^)\/\//, "") +
        "/continue"
    ); // remove protocol from url

    ws.onopen = () => {
      console.log("Connected to the WebSocket");
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const message = data.message;
      const status = data.status;

      if (status == "ERROR") {
        console.log(data);
        ws.close();
      } else if (status == "DONE") {
        ws.close();
      } else setMessage((prevMessage) => `${prevMessage}${message}`);
    };

    ws.onclose = () => {
      console.log("Disconnected from the WebSocket");
    };

    return () => {
      ws.close();
    };
  }, []);

  return (
    <aside>
      <h2>Did you know?</h2>
      <p className="tal">{message}</p>
    </aside>
  );
};

export default FunFact;
