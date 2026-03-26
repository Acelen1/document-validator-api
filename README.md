# Document Validator API

Un progetto Python per la **validazione automatica dei documenti dei lavoratori**, con backend FastAPI e interfaccia web Streamlit.

---

## 🚀 Funzionalità

### Backend (FastAPI)
- Aggiunta di documenti (`POST /api/v1/documents`)
- Aggiornamento di documenti (`PUT /api/v1/documents/{id}`)
- Cancellazione di documenti (`DELETE /api/v1/documents/{id}`)
- Recupero di tutti i documenti (`GET /api/v1/documents`)
- Recupero di un singolo documento (`GET /api/v1/documents/{id}`)
- Validazione dei documenti in base a regole YAML (`POST /api/v1/documents/validate`)
- Visualizzazione dei documenti validati (`GET /api/v1/documents/results`)

### Frontend (Streamlit)
- Visualizzazione dei documenti già validati
- Form per validare nuovi documenti
- Mostra errori rilevati durante la validazione

---

## 🛠️ Tecnologie

- Python 3.10+
- FastAPI
- SQLAlchemy
- MySQL
- Streamlit
- PyYAML

---

## 💻 Installazione

1. Clona il repository:

```bash
git clone https://github.com/Acelen1/document-validator-api.git
cd document-validator-api
