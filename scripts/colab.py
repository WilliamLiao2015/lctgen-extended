from imports.system import os, sys
from imports.packages import genai, openai


in_colab = "google.colab" in sys.modules


def setup_colab():
    if not in_colab: raise Exception("This function is only needed in Google Colab.")

    # Google Colab secrets
    from google.colab import userdata

    # Set up the Google Generative AI authentification
    genai.configure(api_key=userdata.get("GOOGLE_API_KEY"))

    # Set up the OpenAI authentification
    openai.organization = userdata.get("OPENAI_ORGANIZATION")
    openai.api_key = userdata.get("OPENAI_API_KEY")

    os.environ["MONGODB_PASSWORD"] = userdata.get("MONGODB_PASSWORD")
    os.environ["TOGETHER_API_KEY"] = userdata.get("TOGETHER_API_KEY")
