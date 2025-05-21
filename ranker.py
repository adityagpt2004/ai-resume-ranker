import os
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 🧠 Extract text from PDF file
def extract_text_from_pdf(path):
    text = ""
    with open(path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

# ✅ Main function to rank resumes
def rank_resumes(job_description_text, list_of_pdf_filepaths):
    resumes_text = []
    filenames = []

    # Loop through each uploaded resume
    for path in list_of_pdf_filepaths:
        text = extract_text_from_pdf(path)
        resumes_text.append(text)
        filenames.append(os.path.basename(path))  # get 'resume1.pdf'

    # Combine job description and resumes
    documents = [job_description_text] + resumes_text

    # Vectorize all documents
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Compare job description (first vector) with each resume
    job_vec = tfidf_matrix[0]
    resume_vecs = tfidf_matrix[1:]
    similarity_scores = cosine_similarity(job_vec, resume_vecs).flatten()

    # Zip filenames with scores
    results = list(zip(filenames, similarity_scores))

    # Sort from most to least relevant
    results.sort(key=lambda x: x[1], reverse=True)

    return results  # Format: [('resume1.pdf', 0.89), ...]

