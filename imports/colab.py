from imports import sys


in_colab = "google.colab" in sys.modules


if in_colab:
    # Google Colab
    from google.colab import userdata
