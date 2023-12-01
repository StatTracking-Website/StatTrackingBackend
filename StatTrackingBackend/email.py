import mailtrap as mt


def load_template(file_name: str, variables: dict[str, str]):
    with open("StatTrackingBackend/templates/" + file_name + ".html", mode="r", encoding="utf-8") as file:
        content = file.read()
        for var in variables:
            content = content.replace("{{" + var + "}}", variables[var])
        return content


def load_text(file_name: str, variables: dict[str, str]):
    with open("StatTrackingBackend/templates/" + file_name + ".txt", mode="r", encoding="utf-8") as file:
        content = file.read()
        for var in variables:
            content = content.replace("{{" + var + "}}", variables[var])
        return content


def send_generic_email(email_type: str, email: str, subject: str, variables: dict[str, str]):
    mail = mt.Mail(
        sender=mt.Address(email="noreply@stattracking.website", name="StatTracking.Website"),
        to=[mt.Address(email=email)],
        subject=subject,
        text=load_text(email_type, variables),
        html=load_template(email_type, variables)
    )

    client = mt.MailtrapClient(token="e1e733c8f8ac17d1c9388c3f5a03969b")
    client.send(mail)


def send_confirm_email(email: str, user_name: str, confirm_code: str):
    button_link = "https://stattracking.website/callback/confirm-email?verification=" + confirm_code
    send_generic_email("email_confirm", email, "Registration", {"user_name": user_name, "button_link": button_link})


def send_password_reset_email(email: str, user_name: str, reset_code: str):
    button_link = "https://stattracking.website/callback/reset-password?verification=" + reset_code
    send_generic_email("email_password", email, "Reset Password", {"user_name": user_name, "button_link": button_link})
