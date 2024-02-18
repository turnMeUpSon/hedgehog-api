import React, { useState, useEffect } from 'react';

function PingTest() {
  const [pingResponse, setPingResponse] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    // Fetch secured endpoint data
    const fetchPingData = async () => {
      try {
        const token = localStorage.getItem('accessToken');
        const response = await fetch('/api/v1/ping/', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        if (response.ok) {
          const data = await response.json();
          setPingResponse(data.data);
        } else {
          setError('Failed to fetch ping data');
        }
      } catch (error) {
        console.error('Error fetching ping data:', error);
        setError('Failed to fetch ping data');
      }
    };

    fetchPingData();
  }, []); // Run once on component mount

  return (
    <div>
      <h2>Ping Test</h2>
      {pingResponse && <p>{pingResponse}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}

export default PingTest;
