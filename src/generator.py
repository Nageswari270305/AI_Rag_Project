import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def generate_answer(question, retrieved_chunks):

    context_parts = []

    for chunk in retrieved_chunks:

        text = chunk.payload["text"]
        document = chunk.payload["document"]
        page = chunk.payload["page"]

        context_parts.append(
            f"""
Document: {document}
Page: {page}

{text}
"""
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are a legal contract document assistant.

Answer the user's question ONLY using the
provided document context.

Do NOT use outside knowledge.

If the answer cannot be found in the provided
documents, say:

"I couldn't find this information in the
provided contract documents."

Keep the answer clear and concise.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text