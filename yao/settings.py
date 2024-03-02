import os

CLIENT_SECRET = os.getenv("CLIENT_SECRET")
if CLIENT_SECRET is None:
    raise ValueError("CLIENT_SECRET en variable must be set")

YAO_USER_ID = os.getenv("YAO_USER_ID", "<@1031124960229457971>")
GIGUE_URL = os.getenv("GIGUE_URL", "https://www.youtube.com/watch?v=n_iivGo83Ts")
TUDUDU_URL = os.getenv("TUDUDU_URL", "https://youtu.be/U-QZbSPhmQo")
