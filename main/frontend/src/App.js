import React, { useEffect, useState } from 'react';

function App() {
  const [notes, setNotes] = useState([]);
  const [form, setForm] = useState({ title: '', content: '' });
  const [search, setSearch] = useState('');

  // Загрузка заметок с сервера
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
        console.error("API не вернул массив заметок.");
      }
    })
    .catch(err => {
      console.error("Ошибка загрузки заметок:", err);
      setNotes([]);
    });
};

  // Первый запуск
  useEffect(() => {
    fetchNotes();
  }, []);

  // Поиск по мере ввода
  useEffect(() => {
    const delay = setTimeout(() => {
      fetchNotes(search);
    }, 400);
    return () => clearTimeout(delay);
  }, [search]);

  // Отправка новой заметки
  const handleSubmit = (e) => {
    e.preventDefault();

    fetch('http://127.0.0.1:8000/api/notes/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    })
      .then(res => res.json())
      .then(() => {
        setForm({ title: '', content: '' });
        setSearch('');       // ⬅️ сброс фильтра
        fetchNotes();        // ⬅️ загрузка всех заново
      });
  };

  return (
    <div style={{ maxWidth: 600, margin: '0 auto', padding: 20 }}>
      <h2>Заметки</h2>

      <input
        type="text"
        placeholder="Поиск по заголовку или описанию..."
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
        <button type="submit">Добавить</button>
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
