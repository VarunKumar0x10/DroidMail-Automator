from flask import Flask, render_template, request, redirect, url_for
import subprocess
import time

app = Flask(__name__)

def run_adb(command):
    subprocess.run(["adb", "shell"] + command.split(), check=True)

def run_droidrun(prompt):
    subprocess.run(
        [
            "droidrun",
            "run",
            prompt,
            "--provider",
            "OpenRouter",
            "--model",
            "meta-llama/llama-3.3-70b-instruct:free"
        ],
        check=True
    )

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    automation_type = request.form.get("automation_type")

    if automation_type == "email":
        email_to = request.form.get("email_to")
        email_prompt = request.form.get("email_prompt")

        run_adb("am start -n com.google.android.gm/.ConversationListActivityGmail")
        time.sleep(3)

        droidrun_prompt = f"""
        Generate a professional business email based on:
        "{email_prompt}"

        Then perform these steps on Gmail:
        - Tap Compose
        - Enter recipient {email_to}
        - Fill subject and body professionally
        - Do NOT send the email
        """

        run_droidrun(droidrun_prompt)

    elif automation_type == "whatsapp":
        contact = request.form.get("wa_contact")
        wa_prompt = request.form.get("wa_prompt")

        run_adb("am start -n com.whatsapp/.Main")
        time.sleep(4)

        droidrun_prompt = f"""
        Generate a polite WhatsApp business message based on:
        "{wa_prompt}"

        Then perform these steps on WhatsApp:
        - Search for contact "{contact}"
        - Open the chat
        - Type the generated message in the input box
        - Do NOT press send
        """

        run_droidrun(droidrun_prompt)

    return redirect(url_for("success"))

@app.route("/success")
def success():
    return "<h2>Automation executed. Please check the Android.</h2>"

if __name__ == "__main__":
    app.run(debug=True)
