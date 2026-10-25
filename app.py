import streamlit as st
from ollama import chat

SKILLS = [
    "Python",
    "SQL",
    "machine learning",
    "deep learning",
    "natural language processing",
    "NLP",
    "generative AI",
    "LLM",
    "RAG",
    "prompt engineering",
    "LangChain",
    "PyTorch",
    "TensorFlow",
    "pandas",
    "scikit-learn",
    "Git",
    "Docker",
    "REST API",
    "AWS",
]


def find_skills(text):
    text_lower = text.lower()
    return [skill for skill in SKILLS if skill.lower() in text_lower]


def find_evidence(text, skill):
    for sentence in text.replace("\n", " ").split("."):
        if skill.lower() in sentence.lower():
            return sentence.strip()
    return None


def get_evidence_summary(evidence_text):
    response = chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "system",
                "content": (
                    "Summarize only the exact résumé evidence provided. "
                    "Do not add facts, infer skill levels, or judge job fit. "
                    "Do not give advice or define skill names."
                ),
            },
            {
                "role": "user",
                "content": f"""
Write one or two neutral sentences combining these résumé excerpts.
Preserve their meaning and use only the information shown.

RÉSUMÉ EVIDENCE:
{evidence_text}
""",
            },
        ],
    )

    return response.message.content


st.title("CareerLens")
st.write("Compare a résumé with a job description.")

resume = st.text_area(
    "Your résumé",
    height=250,
    placeholder="Paste résumé text here...",
)

job_description = st.text_area(
    "Job description",
    height=250,
    placeholder="Paste the job description here...",
)

if st.button("Analyze match"):
    if not resume.strip() or not job_description.strip():
        st.warning("Please fill in both text boxes.")
    else:
        job_skills = find_skills(job_description)
        resume_skills = find_skills(resume)

        matched = [
            skill for skill in job_skills if skill in resume_skills
        ]
        missing = [
            skill for skill in job_skills if skill not in resume_skills
        ]

        st.subheader("Keyword comparison")

        if not job_skills:
            st.info(
                "No skills from the app's current list were detected "
                "in the job description."
            )
        else:
            st.metric(
                "Listed job skills found in résumé",
                f"{len(matched)} of {len(job_skills)}",
            )

            st.write("**Résumé evidence for detected skills:**")

            evidence_lines = []
            for skill in matched:
                evidence = find_evidence(resume, skill)
                if evidence:
                    evidence_lines.append(f"- **{skill}:** {evidence}")

            if evidence_lines:
                st.markdown("\n".join(evidence_lines))
            else:
                st.write("None detected")

            st.write("**Found in both:**")
            st.write(", ".join(matched) if matched else "None detected")

            st.write("**In job description, not detected in résumé:**")
            st.write(", ".join(missing) if missing else "None detected")

        st.subheader("Local AI evidence summary")

        if matched:
            evidence_text = "\n".join(
                f"- {skill}: {find_evidence(resume, skill)}"
                for skill in matched
                if find_evidence(resume, skill)
            )

            try:
                with st.spinner("Summarizing résumé evidence locally..."):
                    summary = get_evidence_summary(evidence_text)

                st.caption(
                    "AI-generated summary. Check it against the evidence above."
                )
                st.write(summary)
            except Exception as error:
                st.error("The local AI summary could not be generated.")
                st.caption(str(error))
        else:
            st.info("No matched résumé evidence is available to summarize.")