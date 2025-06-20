import React, { useEffect, useState } from 'react';

function App() {
  const [notes, setNotes] = useState([]);
  const [form, setForm] = useState({ title: '', content: '' });

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/notes/')
      .then(res => res.json())
      .then(data => setNotes(data));
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch('http://127.0.0.1:8000/api/notes/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    })
      .then(res => res.json())
      .then(newNote => {
        setNotes([newNote, ...notes]);
        setForm({ title: '', content: '' });
      });
  };

  return (
    <div style={{ maxWidth: 600, margin: '0 auto', padding: 20 }}>
      <h2>Заметки</h2>

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
        {notes.map(note => (
          <li key={note.id}>
            <strong>{note.title}</strong><br />
            {note.content}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
