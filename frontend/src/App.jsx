import { Analytics } from "@vercel/analytics/react";
import Header from "./Header.jsx";
// import NavBar from "./NavBar.jsx";
import "./App.css";

function App() {
  return (
    <>
      {/* <NavBar /> */}
      <Header />
      <Analytics />
    </>
  );
}

export default App;
