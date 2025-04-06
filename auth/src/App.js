import React from 'react';
import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';

function App() {
  return (
      <div>
        <h1>Auth Service</h1>
        <RegisterForm />
        <LoginForm />
      </div>
  );
}

export default App;
