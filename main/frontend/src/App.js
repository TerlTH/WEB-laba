import React, { useEffect, useState } from 'react';

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function App() {
  const API = 'http://localhost:8000/api';

  const [selectedTab, setSelectedTab] = useState('notes');
  const [notes, setNotes] = useState([]);
  const [products, setProducts] = useState([]);
  const [form, setForm] = useState({ title: '', content: '', file: null, price: '' });
  const [registerForm, setRegisterForm] = useState({ username: '', password: '', age: '' });
  const [loginForm, setLoginForm] = useState({ username: '', password: '' });
  const [user, setUser] = useState(null);
  const [editNoteId, setEditNoteId] = useState(null);

  // 🟢 Вызов при загрузке страницы — проверка авторизации
  useEffect(() => {
    fetchProfile();
  }, []);

  // 🔄 Загрузка данных при смене вкладки (если пользователь уже авторизован)
  useEffect(() => {
    if (user) {
      selectedTab === 'notes' ? fetchNotes() : fetchProducts();
    }
  }, [selectedTab, user]);

  const fetchNotes = () => {
    fetch(`${API}/notes/`)
      .then(res => res.json())
      .then(data => setNotes(Array.isArray(data) ? data : data.results));
  };

  const fetchProducts = () => {
    fetch(`${API}/products/`)
      .then(res => res.json())
      .then(data => setProducts(Array.isArray(data) ? data : data.results));
  };

  const fetchProfile = () => {
    fetch(`${API}/users/profile/`, { credentials: 'include' })
      .then(res => res.ok ? res.json() : Promise.reject())
      .then(data => setUser(data.user))
      .catch(() => setUser(null));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('title', form.title);
    formData.append('content', form.content);
    if (form.file instanceof File) {
      formData.append('file', form.file);
    }
    if (selectedTab === 'products') {
      formData.append('price', form.price || '0');
      formData.append('description', form.content); // 👈 ключевая строка
    }

    const url = selectedTab === 'notes'
      ? (editNoteId ? `${API}/notes/${editNoteId}/` : `${API}/notes/`)
      : `${API}/products/`;
    const method = selectedTab === 'notes' && editNoteId ? 'PUT' : 'POST';

    fetch(url, {
      method,
      credentials: 'include',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: formData,
    })
      .then(res => res.json())
      .then(() => {
        setForm({ title: '', content: '', file: null, price: '' });
        setEditNoteId(null);
        selectedTab === 'notes' ? fetchNotes() : fetchProducts();
      });
  };

  const handleDelete = (id, type) => {
    if (!window.confirm('Удалить?')) return;
    fetch(`${API}/${type}/${id}/`, {
      method: 'DELETE',
      headers: { 'X-CSRFToken': getCookie('csrftoken') },
      credentials: 'include',
    }).then(() => {
      type === 'notes' ? fetchNotes() : fetchProducts();
    });
  };

  const handleAddProductToNotes = (product) => {
    const formData = new FormData();
    formData.append('title', product.title);
    formData.append('content', product.description || '');

    fetch(`${API}/notes/`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: formData,
    }).then(() => {
      alert('Шаблон добавлен в заметки!');
      fetchNotes();
    });
  };

  const handleLogin = (e) => {
    e.preventDefault();
    fetch(`${API}/users/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      credentials: 'include',
      body: JSON.stringify(loginForm),
    })
      .then(res => res.json())
      .then(data => {
        if (data.message === 'Вы вошли') {
          fetchProfile();
        } else {
          alert('Ошибка входа');
        }
      });
  };

  const handleRegister = (e) => {
    e.preventDefault();
    fetch(`${API}/users/register/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      credentials: 'include',
      body: JSON.stringify(registerForm),
    }).then(res => {
      if (res.status === 201) alert('Регистрация успешна');
      else alert('Ошибка регистрации');
    });
  };

  const handleLogout = () => {
    fetch(`${API}/users/logout/`, {
      method: 'POST',
      headers: { 'X-CSRFToken': getCookie('csrftoken') },
      credentials: 'include',
    }).then(() => setUser(null));
  };

  return (
    <div style={{ maxWidth: 700, margin: '0 auto', padding: 20 }}>
      <h2>📌 Сервис заметок</h2>

      {!user && (
        <>
          <form onSubmit={handleRegister}>
            <h4>Регистрация</h4>
            <input placeholder="Логин" onChange={e => setRegisterForm({ ...registerForm, username: e.target.value })} />
            <input placeholder="Пароль" type="password" onChange={e => setRegisterForm({ ...registerForm, password: e.target.value })} />
            <input placeholder="Возраст" type="number" onChange={e => setRegisterForm({ ...registerForm, age: e.target.value })} />
            <button>Зарегистрироваться</button>
          </form>

          <form onSubmit={handleLogin}>
            <h4>Вход</h4>
            <input placeholder="Логин" onChange={e => setLoginForm({ ...loginForm, username: e.target.value })} />
            <input placeholder="Пароль" type="password" onChange={e => setLoginForm({ ...loginForm, password: e.target.value })} />
            <button>Войти</button>
          </form>
        </>
      )}

      {user && (
        <>
          <p>👤 Вы вошли как <b>{user}</b></p>
          <button onClick={handleLogout}>Выйти</button>
        </>
      )}

      <div style={{ margin: '20px 0' }}>
        <button onClick={() => setSelectedTab('notes')}>Мои заметки</button>
        <button onClick={() => setSelectedTab('products')} style={{ marginLeft: 10 }}>Шаблоны</button>
      </div>

      <form onSubmit={handleSubmit}>
        <h4>{selectedTab === 'notes' ? 'Новая заметка' : 'Новый шаблон'}</h4>
        <input placeholder="Заголовок" value={form.title} onChange={e => setForm({ ...form, title: e.target.value })} required />
        <textarea placeholder="Текст" value={form.content} onChange={e => setForm({ ...form, content: e.target.value })} />
        {selectedTab === 'products' && (
          <input type="number" placeholder="Цена" value={form.price} onChange={e => setForm({ ...form, price: e.target.value })} />
        )}
        <input type="file" onChange={e => setForm({ ...form, file: e.target.files[0] })} />
        <button type="submit" disabled={!user}>Сохранить</button>
      </form>

      <hr />
      <h3>{selectedTab === 'notes' ? '📃 Мои заметки' : '📋 Шаблоны'}</h3>

      <ul>
        {(selectedTab === 'notes' ? notes : products).map(item => (
          <li key={item.id} style={{ marginBottom: 15 }}>
            <b>{item.title}</b><br />
            <div style={{ whiteSpace: 'pre-wrap', marginTop: 5 }}>
              {selectedTab === 'notes' ? item.content : item.description}
            </div>
            {item.price && (
              <div style={{ color: 'green', marginTop: 4 }}>
                💰 {item.price} ₽
              </div>
            )}
            <div style={{ marginTop: 5 }}>
              {item.owner === user && (
                <button onClick={() => handleDelete(item.id, selectedTab)}>Удалить</button>
              )}
              {selectedTab === 'products' && (
                <button onClick={() => handleAddProductToNotes(item)} style={{ marginLeft: 10 }}>
                  Добавить в заметки
                </button>
              )}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
