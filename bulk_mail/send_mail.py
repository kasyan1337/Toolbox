import os
import webbrowser
from src.bulk_mail import send_bulk_emails, get_recipients, get_email_body

if __name__ == "__main__":
    # Configuration
    email_sender = "WTM"  # Name of the account as defined in .env
    email_receiver = "recipients.txt"  # Recipients file in the email folder
    subject = "Dopyt cenníkov_Skúška tvrdosti_12032025"  # Enter the email subject directly here
    body = "WTM.html"  # Email body file (body.txt for plain text or body.html for HTML)
    content_folder = "email"

    # Define paths
    email_folder = os.path.join(os.path.dirname(__file__), content_folder)
    recipients_file = os.path.join(email_folder, email_receiver)
    content_path = os.path.join(
        email_folder, "content.txt"
    )  # Specify the content file path
    body_file = os.path.join(email_folder, body)

    # Generate the email body content
    email_body = get_email_body(body_file, content_path=content_path)

    # Save the HTML preview to a temporary file
    preview_file_path = os.path.join(email_folder, "email_preview.html")
    with open(preview_file_path, "w") as preview_file:
        preview_file.write(email_body)

    # Open the preview in Safari
    webbrowser.get("safari").open("file://" + preview_file_path)

    # Load recipients and display for confirmation
    recipients = get_recipients(recipients_file)
    print("\nRecipients:")
    print("\n".join(recipients))

    # Ask for confirmation before proceeding
    confirm = input(
        "\nIs this the correct list of recipients? Type 'Y' to confirm: "
    ).strip()
    if confirm.lower() == "y":
        # Send bulk emails
        send_bulk_emails(
            account_name=email_sender,
            recipients_filename=email_receiver,
            subject=subject,
            body_filename=body,  # Pass body.html directly
            content_path=(
                content_path if "CWT.html" in body or "WTM.html" in body else None
            ),  # Only pass content_path if using a template
        )
        print("Email sent successfully.")
    else:
        print("Email sending cancelled.")

    # Delete the preview file
    if os.path.exists(preview_file_path):
        os.remove(preview_file_path)
        print("Preview file deleted.")
