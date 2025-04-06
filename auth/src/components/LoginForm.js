import React, { useState } from 'react';
import axios from 'axios';

export default function LoginForm() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleLogin = async () => {
        try {
            const res = await axios.post('http://localhost:8000/login', { username, password });
            alert(`✅ Токен: ${res.data.token}`);
        } catch (err) {
            alert('❌ Невірний логін або пароль');
        }
    };

    return (
        <div>
            <h2>Вхід</h2>
            <input placeholder="Логін" value={username} onChange={e => setUsername(e.target.value)} />
            <input type="password" placeholder="Пароль" value={password} onChange={e => setPassword(e.target.value)} />
            <button onClick={handleLogin}>Увійти</button>
        </div>
    );
}
