import "../styles/Footer.css";

function Footer() {
  return (
    <footer>
      <div>
        <h3>Made by Andrew Hinh</h3>
        <a href="https://github.com/andrewhinh/project">
          <img
            src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg"
            alt="Repository Link"
            className="gh-logo"
          />
        </a>
      </div>
      <img
        src="https://storage.googleapis.com/chydlx/codepen/random-gif-generator/giphy-logo.gif"
        alt="Giphy Logo"
        className="giphy-logo"
      />
    </footer>
  );
}

export default Footer;
