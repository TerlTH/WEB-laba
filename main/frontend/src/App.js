import React, { useEffect, useState } from 'react';

function App() {
  const API = 'http://localhost:8000/api';

  const [notes, setNotes] = useState([]);
  const [form, setForm] = useState({ title: '', content: '' });
  const [search, setSearch] = useState('');
  const [registerForm, setRegisterForm] = useState({ username: '', password: '' });
  const [loginForm, setLoginForm] = useState({ username: '', password: '' });
  const [user, setUser] = useState(null);
  const [users, setUsers] = useState([]);
  const [usersPage, setUsersPage] = useState(1);

  const fetchNotes = (query = '') => {
    let url = `${API}/notes/`;
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
        }
      });
  };

  useEffect(() => {
    fetchNotes();
    fetchProfile();
  }, []);

  useEffect(() => {
    const delay = setTimeout(() => {
      fetchNotes(search);
    }, 400);
    return () => clearTimeout(delay);
  }, [search]);

  const handleSubmit = (e) => {
    e.preventDefault();

    fetch(`${API}/notes/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
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

const handleRegister = (e) => {
  e.preventDefault();
  fetch(`${API}/users/register/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(registerForm),
  })
    .then(res => {
      if (res.status === 201) {
        alert('Регистрация успешна. Теперь войдите.');
      } else {
        alert('Ошибка регистрации');
      }
    });
};

  const handleLogin = (e) => {
  e.preventDefault();
  fetch(`${API}/users/login/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(loginForm),
  })
    .then(res => res.json())
    .then(data => {
      if (data.message === 'Вы вошли') {
        alert('Вход выполнен');
        fetchProfile();
      } else {
        alert('Ошибка входа');
      }
    });
};

  const handleLogout = () => {
    fetch(`${API}/users/logout/`, {
      method: 'POST',
      credentials: 'include',
    }).then(() => {
      setUser(null);
      alert('Вы вышли');
    });
  };

const fetchProfile = () => {
  fetch(`${API}/users/profile/`, {
    credentials: 'include',  
  })
    .then(res => {
      if (res.status === 200) return res.json();
      throw new Error();
    })
    .then(data => setUser(data.user))
    .catch(() => setUser(null));
};

  const fetchUsersPage = (page) => {
    fetch(`${API}/users/list/?page=${page}`, {
      credentials: 'include',
    })
      .then(res => res.json())
      .then(data => {
        setUsers(data.results);
        setUsersPage(page);
      });
  };

  return (
    <div style={{ maxWidth: 600, margin: '0 auto', padding: 20 }}>
      <h2>Заметки</h2>

      {!user && (
        <>
          <form onSubmit={handleRegister} style={{ marginBottom: 20 }}>
            <h4>Регистрация</h4>
              <input
                type="text"
                placeholder="Логин"
                value={registerForm.username}
                onChange={e => setRegisterForm({ ...registerForm, username: e.target.value })}
                required
              />
              <input
                type="password"
                placeholder="Пароль"
                value={registerForm.password}
                onChange={e => setRegisterForm({ ...registerForm, password: e.target.value })}
                required
              />
              <button type="submit">Зарегистрироваться</button>
            </form>

          <form onSubmit={handleLogin} style={{ marginBottom: 20 }}>
              <h4>Вход</h4>
              <input
                type="text"
                placeholder="Логин"
                value={loginForm.username}
                onChange={e => setLoginForm({ ...loginForm, username: e.target.value })}
                required
              />
              <input
                type="password"
                placeholder="Пароль"
                value={loginForm.password}
                onChange={e => setLoginForm({ ...loginForm, password: e.target.value })}
                required
              />
              <button type="submit">Войти</button>
            </form>
        </>
      )}

      {user && (
        <>
          <p>👤 Вы вошли как <strong>{user}</strong></p>
          <button onClick={handleLogout}>Выйти</button>

          <div style={{ marginTop: 20 }}>
            <h4>Пользователи (с пагинацией)</h4>
            <button onClick={() => fetchUsersPage(usersPage - 1)} disabled={usersPage <= 1}>←</button>
            <button onClick={() => fetchUsersPage(usersPage + 1)}>→</button>
            <ul>
              {users.map(u => (
                <li key={u.username}>{u.username} ({u.email})</li>
              ))}
            </ul>
          </div>
        </>
      )}

      <input
        type="text"
        placeholder="Поиск..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        style={{ width: '100%', marginBottom: 10 }}
      />

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
        <button type="submit" disabled={!user}>Добавить</button>
      </form>

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
