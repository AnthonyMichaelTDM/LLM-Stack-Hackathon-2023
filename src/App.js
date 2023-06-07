import './styles/App.css';

import Header from './components/header.js';
import FileUploader from './components/file.js';
import UrlUploader from './components/url.js';
import ChatBox from './components/chat.js';

function App() {
  return (
    <div className="App">
      <Header />
      <FileUploader />
      <UrlUploader />
      <ChatBox />
    </div>
  );
}

export default App;
