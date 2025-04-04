"use client";

import React, { useState } from 'react';
import {DisplayResults} from './results'

require('dotenv').config();


const SearchBar: React.FC = () => {
  const [query, setQuery] = useState<string>(''); // search input state
  const [result, setResult] = useState<string>(''); // stores endpoint response
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const backend_url = process.env.NEXT_PUBLIC_BACKEND;

    console.log(backend_url)

    try {
      const response = await fetch(`${backend_url}test/${query.startsWith('https://') ? query : `https://${query}`}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'same-origin', 
      });
    
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.text();
      setResult(data);
    } catch (err) {
      setError((err as Error).message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };
  

  return (
    <div>
      <form onSubmit={handleSearch} className="flex justify-center w-full">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter search..."
          className="border border-gray-300 rounded-l px-4 py-2 w-80 focus:outline-none focus:ring-2 focus:ring-brown-500"
        />
        <button 
          type="submit"
          className="bg-brown-500 text-white px-4 py-2 rounded-r hover:bg-brown-600 focus:outline-none focus:ring-2 focus:ring-brown-500"
        >
          Search
        </button>
      </form>
      
      {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
      
      {result && (
        <div>
          <h3>Response:</h3>
          <pre className="bg-gray-100 p-4 rounded overflow-auto max-h-96 w-full max-w-4xl">
            <DisplayResults jsonData={JSON.parse(result)}/>
          </pre>
        </div>
      )}
    </div>
  );
};

export default SearchBar;