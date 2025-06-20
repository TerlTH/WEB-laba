import React, { useEffect, useState } from 'react';

function App() {
  const [notes, setNotes] = useState([]);
  const [form, setForm] = useState({ title: '', content: '' });
  const [search, setSearch] = useState('');
  const [auth, setAuth] = useState({ username: '', password: '' });
  const [token, setToken] = useState(localStorage.getItem('token') || '');

  const fetchNotes = (query = '') => {
    let url = 'http://127.0.0.1:8000/api/notes/';
    if (query) {
      url += `?search=${encodeURIComponent(query)}`;
    }

    fetch(url)
      .then(res => res.json())
      .then(data => {
        const notesList = Array.isArray(data) ? data : data.results;
        if (Array.isArray(notesList)) {
          setNotes(notesList);
        } else {
          setNotes([]);
          console.error('API не вернул массив заметок.');
        }
      })
      .catch(err => {
        console.error('Ошибка загрузки заметок:', err);
        setNotes([]);
      });
  };

  useEffect(() => {
    fetchNotes();
  }, []);

  useEffect(() => {
    const delay = setTimeout(() => {
      fetchNotes(search);
    }, 400);
    return () => clearTimeout(delay);
  }, [search]);

  const handleLogin = (e) => {
    e.preventDefault();

    fetch('http://127.0.0.1:8000/api-token-auth/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(auth),
    })
      .then(res => res.json())
      .then(data => {
        if (data.token) {
          localStorage.setItem('token', data.token);
          setToken(data.token);
          alert('Вы успешно вошли в систему');
        } else {
          alert('Ошибка авторизации');
        }
      })
      .catch(() => alert('Ошибка соединения с сервером'));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    fetch('http://127.0.0.1:8000/api/notes/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${token}`,
      },
      body: JSON.stringify(form),
    })
      .then(res => {
        if (res.status === 401) {
          alert('Вы не авторизованы');
          return null;
        }
        return res.json();
      })
      .then(newNote => {
        if (newNote) {
          setForm({ title: '', content: '' });
          setSearch('');
          fetchNotes();
        }
      });
  };

  return (
    <div style={{ maxWidth: 600, margin: '0 auto', padding: 20 }}>
      <h2>Заметки</h2>

      {/* 🔐 Форма входа */}
      {!token && (
        <form onSubmit={handleLogin} style={{ marginBottom: 20 }}>
          <h4>Вход</h4>
          <input
            type="text"
            placeholder="Логин"
            value={auth.username}
            onChange={e => setAuth({ ...auth, username: e.target.value })}
            required
          />
          <br />
          <input
            type="password"
            placeholder="Пароль"
            value={auth.password}
            onChange={e => setAuth({ ...auth, password: e.target.value })}
            required
          />
          <br />
          <button type="submit">Войти</button>
        </form>
      )}

      {/* 🔍 Поиск */}
      <input
        type="text"
        placeholder="Поиск..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        style={{ width: '100%', marginBottom: 10 }}
      />

      {/* ➕ Форма добавления заметки */}
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Заголовок"
          value={form.title}
          onChange={e => setForm({ ...form, title: e.target.value })}
          required
        />
        <br />
        <textarea
          placeholder="Описание"
          value={form.content}
          onChange={e => setForm({ ...form, content: e.target.value })}
        />
        <br />
        <button type="submit" disabled={!token}>Добавить</button>
      </form>

      {/* 📄 Список заметок */}
      <ul>
        {Array.isArray(notes) && notes.length > 0 ? (
          notes.map(note => (
            <li key={note.id}>
              <strong>{note.title}</strong><br />
              {note.content}
            </li>
          ))
        ) : (
          <p style={{ color: 'gray' }}>Нет заметок для отображения.</p>
        )}
      </ul>
    </div>
  );
}

export default App;
