import { Analytics } from "@vercel/analytics/react";
import Header from "./Header.jsx";
import "./App.css";

function App() {
  return (
    <>
      <Header />
      <Analytics />
    </>
  );
}

export default App;
