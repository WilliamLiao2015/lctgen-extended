from imports import sys, genai


def setup_colab():
    in_colab = "google.colab" in sys.modules

    if not in_colab: raise Exception("This function is only needed in Google Colab.")

    # Google Colab
    from google.colab import userdata
    genai.configure(api_key=userdata.get("GOOGLE_API_KEY"))
