import React, { useState } from 'react';
import axios from 'axios';

function Signup() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [password2, setPassword2] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    // Check if passwords match
    if (password !== password2) {
      setError('Passwords do not match');
      return;
    }
    // Send registration request to the server
    try {
      const response = await axios.post('http://localhost:8000/auth_service_jwt/v1/signup/', {
        username: username,
        password: password,
        password2: password2,
      },
      {
        headers: {
            'Content-Type': 'application/json',
          },
      });
      if (response.status === 201) {
        // Handle successful registration
        console.log('Registration successful');
      } else {
        // Handle registration failure
        console.error('Registration failed:', response.data); // Log response data for debugging
      }
    } catch (error) {
      console.error('Error registering:', error);
    }
  };

  return (
    <div>
      <h2>Registration</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
        <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <input type="password" placeholder="Confirm Password" value={password2} onChange={(e) => setPassword2(e.target.value)} />
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <button type="submit">Register</button>
      </form>
    </div>
  );
}

export default Signup;

