import React, { useState } from 'react';
import axios from 'axios';

export default function RegisterForm() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleRegister = async () => {
        try {
            const res = await axios.post('http://localhost:8000/register', { username, password });
            alert(res.data.message);
        } catch (err) {
            alert('❌ Реєстрація не вдалася');
        }
    };

    return (
        <div>
            <h2>Реєстрація</h2>
            <input placeholder="Логін" value={username} onChange={e => setUsername(e.target.value)} />
            <input type="password" placeholder="Пароль" value={password} onChange={e => setPassword(e.target.value)} />
            <button onClick={handleRegister}>Зареєструватися</button>
        </div>
    );
}
