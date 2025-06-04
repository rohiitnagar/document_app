
import streamlit as st
import openai

openai.api_key = "Ysk-proj-fyimFojPXD837qIauS7DHvxTUErdh6YVLLQxsl1o8O9rU2lgXe1xCQ3tx7_CPZXOt51ufkyoKFT3BlbkFJIF5wHOzZe5FzntDTUNzBdDbmcEBOWJn9l1PnJBG9-jv3w0vT9h28FuH83BpLXhBZPR826cEugA"  # Replace this

st.title("🧠 Document Similarity Comparison & Ranking")

job_description = st.text_area("Paste Job Description:")

st.write("Upload Consultant Profiles (TXT or DOCX only):")
uploaded_files = st.file_uploader("Choose files", type=["txt", "docx"], accept_multiple_files=True)

def extract_text(file):
    if file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    elif file.name.endswith(".docx"):
        from docx import Document
        doc = Document(file)
        return "\n".join([p.text for p in doc.paragraphs])
    return ""

def compare_with_openai(job, profile):
    prompt = f"Compare this job description:\n{job}\n\nWith this consultant profile:\n{profile}\n\nGive a match score out of 100 based on skills, experience, and relevance."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return int(''.join(filter(str.isdigit, response['choices'][0]['message']['content']))[:3])

if st.button("Compare and Rank"):
    if not job_description or not uploaded_files:
        st.warning("Please provide both job description and consultant profiles.")
    else:
        results = []
        for file in uploaded_files:
            profile_text = extract_text(file)
            score = compare_with_openai(job_description, profile_text)
            results.append((file.name, score))
        results.sort(key=lambda x: x[1], reverse=True)
        st.subheader("🔝 Top Matches:")
        for i, (name, score) in enumerate(results[:3]):
            st.write(f"{i+1}. **{name}** — Match Score: {score}/100")
        if all(score < 40 for _, score in results):
            st.warning("⚠️ No suitable candidates found.")
