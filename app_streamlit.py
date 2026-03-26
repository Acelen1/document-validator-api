import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/api/v1"

st.title("Pipeline di Validazione Documenti")

st.header("1️⃣ Vedi tutti i documenti validati")

# GET sicuro
try:
    response = requests.get(f"{API_URL}/documents/results")

    if response.status_code == 200:
        try:
            validated_documents = response.json()
            if isinstance(validated_documents, dict):
                validated_documents = [validated_documents]
        except:
            st.error("❌ Il backend non restituisce JSON valido")
            st.write(response.text)
            validated_documents = []
    else:
        st.error(f"❌ Errore backend: {response.status_code}")
        st.write(response.text)
        validated_documents = []

except Exception as e:
    st.error(f"❌ Backend non raggiungibile: {e}")
    validated_documents = []

# Mostra dati
if validated_documents:
    for doc in validated_documents:
        st.subheader(f"Documento: {doc.get('worker_name','N/A')} (ID: {doc.get('document_id','N/A')})")
        status = doc.get("status", "unknown")
        st.write(f"**Status:** {'✅ Valid' if status=='valid' else '❌ Invalid'}")

        if doc.get("errors"):
            st.write("**Errori:**")
            for err in doc["errors"]:
                st.write(f"- {err}")
else:
    st.info("Nessun documento validato ancora.")

# -------------------------
# FORM VALIDAZIONE
# -------------------------
st.header("2️⃣ Valida un nuovo documento")

with st.form("validate_form"):
    worker_name = st.text_input("Nome lavoratore")
    training_completed = st.checkbox("Training completato")
    medical_certificate = st.checkbox("Certificato medico valido")

    submitted = st.form_submit_button("Valida documento")

    if submitted:
        payload = {
            "worker_name": worker_name,
            "training_completed": training_completed,
            "medical_certificate": medical_certificate,
            "middle_name": None
        }

        try:
            r = requests.post(f"{API_URL}/documents/validate", json=payload)

            if r.status_code == 200:
                try:
                    result = r.json()
                    st.success(f"✅ Documento validato! Status: {result.get('status','unknown')}")

                    if result.get("errors"):
                        st.write("Errori:")
                        for err in result["errors"]:
                            st.write(f"- {err}")

                except:
                    st.error("❌ Risposta NON JSON dal backend")
                    st.write(r.text)

            else:
                st.error(f"❌ Errore backend: {r.status_code}")
                st.write(r.text)

        except Exception as e:
            st.error(f"❌ Errore connessione: {e}")