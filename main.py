from flask import Flask, render_template, request
from flask_mail import Mail, Message
from decouple import config

app = Flask(__name__)

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=config('MAIL_USERNAME'),
    MAIL_PASSWORD=config('MAIL_PASSWORD')
)

mail = Mail(app)


def send_contact_form(result):
    msg = Message("Contact Form from Website",
                  sender=config('MAIL_USERNAME'),
                  recipients=[config('MAIL_USERNAME')])

    msg.body = """
    Hello there,
    
    You just received a contact form.
    
    Name: {}
    Email: {}
    Phone: {}
    Message: {}
    
    Regards,
    Renata's Website
    
    """.format(result['name'], result['email'], result['phone'], result['message'])

    mail.send(msg)


@app.route('/', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        result = {'name': request.form['name'],
                  'email': request.form['email'].replace(' ', '').lower(),
                  'phone': request.form['phone'],
                  'message': request.form['message']}

        send_contact_form(result)

        return render_template('index.html')

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
