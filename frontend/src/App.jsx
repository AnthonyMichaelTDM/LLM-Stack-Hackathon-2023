import { Analytics } from "@vercel/analytics/react";
import Header from "./components/Header.jsx";
import Main from "./components/Main.jsx";
import Footer from "./components/Footer.jsx";
import "./styles/App.css";

function App() {
  return (
    <>
      <Header />
      <Main />
      <Footer />
      <Analytics />
    </>
  );
}

export default App;
