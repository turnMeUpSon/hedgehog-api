import React from 'react';

function Logout() {
  const handleLogout = async () => {
    // Send logout request to the server
    try {
      const response = await fetch('/api/v1/logout/', {
        method: 'POST'
      });
      if (response.ok) {
        // Handle successful logout
        console.log('Logout successful');
      } else {
        // Handle logout failure
        console.error('Logout failed');
      }
    } catch (error) {
      console.error('Error logging out:', error);
    }
  };

  return (
    <div>
      <h2>Logout</h2>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
}

export default Logout;
