from dotenv import load_dotenv
load_dotenv()
import os
from nylas import APIClient

os.environ["CLIENT_ID"] = "2ptm3q4vfhep6576ndyl8kjp7"
os.environ["CLIENT_SECRET"] = "aunp2lc6r66zz3cnvuzuhkvvc"
os.environ["ACCESS_TOKEN"] = "YCMzFvN8g4fhijt7aNqBFr7mkUEhy6"
def send_mail(name,email,body_des):
    nylas = APIClient(
        os.environ.get("CLIENT_ID"),
        os.environ.get("CLIENT_SECRET"),
        os.environ.get("ACCESS_TOKEN"),
    )
    draft = nylas.drafts.create()
    draft.subject = "Workout Report from Fitness Corner"
    draft.body = body_des+"Stay motivated and keep up the good work with Fitness Corner!"
    draft.to = [{"name": name, "email": email}]
    draft.send()
