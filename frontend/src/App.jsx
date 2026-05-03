import React from 'react';
import Search from './components/Search'; // Importing your component!

function App() {
  return (
    <div className="App">
      <header style={{ padding: '20px', background: '#f4f4f4' }}>
        <h1>Project NOVA: Semantic Search</h1>
      </header>
      <main>
        <Search /> 
      </main>
    </div>
  );
}

export default App;