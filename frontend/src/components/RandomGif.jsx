// eslint-disable-next-line no-unused-vars
import React, { useState, useEffect } from "react";
import "../styles/RandomGif.css";

const RandomGif = () => {
  const [url, setUrl] = useState(null); // Declare a state for the URL

  const giphy = {
    baseURL: "https://api.giphy.com/v1/gifs/random",
    apiKey: import.meta.env.VITE_GIPHY_API_KEY,
    rating: "r",
  };

  let giphyURL = encodeURI(
    `${giphy.baseURL}?api_key=${giphy.apiKey}&rating=${giphy.rating}`
  );

  useEffect(() => {
    const getGifURL = async () => {
      let response = await fetch(giphyURL, {
        mode: "cors",
        method: "GET",
        headers: {
          "Content-type": "application/json; charset=UTF-8",
        },
      });
      response = await response.json();
      const fetchedUrl = response.data.images.original.url;
      setUrl(fetchedUrl); // Set the state
    };

    getGifURL();
  }, [giphyURL]);

  return (
    <aside>
      {url ? <img src={url} alt="Random Gif" className="gif" /> : "Loading..."}
    </aside>
  );
};

export default RandomGif;
