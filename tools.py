
from ai_engine import generate_answer
from prompts import FEATURE_PROMPTS


def run_feature(feature, user_text):

    instruction = FEATURE_PROMPTS.get(feature)

    if not instruction:
        raise ValueError("Fitur tidak ditemukan.")

    prompt = f"""
    {instruction}

    Permintaan pengguna:
    {user_text}
    """

    answer, model = generate_answer(prompt)

    return answer, model


def summarize_text(text):

    return run_feature("Ringkas", text)


def translate_text(text, language):

    prompt = (
        f"Terjemahkan teks berikut ke {language}:\n\n{text}"
    )

    return generate_answer(prompt)


def coding_help(question):

    return run_feature("Coding", question)


def study_help(question):

    return run_feature("Belajar", question)


def report_help(question):

    return run_feature("Laporan", question)
