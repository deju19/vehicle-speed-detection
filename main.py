from flask import Flask,request,render_template,redirect,url_for
import cv2
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
import os
app = Flask(__name__)
'''def report_send_mail(mailid1,message):
    
    
    #label = "Eye Close"
    #with open(image_path, 'rb') as f:
        #img_data = f.read()
    fromaddr = "sdprotrichy2k23@gmail.com"
    toaddr = mailid1
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Alert"
    body = message
    msg.attach(MIMEText(body, 'plain'))  # attach plain text
    #image = MIMEImage(img_data, name=os.path.basename(image_path))
    #msg.attach(image) # attach image
    s = smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login(fromaddr, "xwycjezbamzaroti")
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()'''

def report_send_mail(msg12):
    # Email login credentials
    email_address = "sdprotrichy2k23@gmail.com"
    email_password = "wxyz"

    # Email recipients
    to_email_list = ['midhuntp17@gmail.com','midhunprakash.ae19@bitsathy.ac.in','shaveena.ae19@bitsathy.ac.in','saviraj252002@gmail.com','dejasshri.ae19@bitsathy.ac.in']

    # Create a message object
    msg = MIMEMultipart()

    # Add the message body
    msg.attach(MIMEText(msg12))

    # Set the email subject, sender, and recipients
    msg['Subject'] = "alert "
    msg['From'] = email_address
    msg['To'] = ", ".join(to_email_list)

    # Connect to the SMTP server
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(email_address, email_password)

        # Send the email to multiple recipients
        smtp.sendmail(email_address, to_email_list, msg.as_string())

        print("Email sent successfully!")
@app.route('/')
def home():
    return render_template('adminlogin1.html')

@app.route('/validatenew',methods=['POST','GET'])
def validatenew():
    if request.method == 'POST':
        uname = request.form.get('uname')
        upass = request.form.get('password')
        if uname == 'admin' and upass == '1234':
            return render_template('index1.html')
        else:
            return render_template('adminlogin1.html',msg='Invalid Username or Password')


@app.route('/detect')
def detect():
    weights_path = "yolo-coco\yolov3.weights"
    config_path = "yolo-coco\yolov3.cfg"
    net = "(config_path, weights_path)"

    # Load COCO dataset class names
    classes = []
    with open("dataset\yolo-coco\coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    cascade_src = 'dataset/cars1.xml'
    video_src = 'dataset/video3.MP4'

    ax1 = 70
    ay = 90
    ax2 = 230

    bx1 = 15
    by = 125
    bx2 = 225
    xy = 10

    def Speed_Cal(time):

        try:
            # Speed = (9.144*3600)/(time*1000)
            Speed = (9.875 * 3600) / (time * 1000)
            return Speed
        except ZeroDivisionError:
            print(5)

    i = 1
    start_time = time.time()

    cap = cv2.VideoCapture(video_src)
    car_cascade = cv2.CascadeClassifier(cascade_src)

    while True:
        ret, img = cap.read()
        if (type(img) == type(None)):
            break

        blurred = cv2.blur(img, ksize=(15, 15))
        gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
        cars = car_cascade.detectMultiScale(gray, 1.1, 2)

        cv2.line(img, (ax1, ay), (ax2, ay), (255, 0, 0), 2)

        cv2.line(img, (bx1, by), (bx2, by), (255, 0, 0), 2)

        for (x, y, w, h) in cars:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.circle(img, (int((x + x + w) / 2), int((y + y + h) / 2)), 1, (0, 255, 0), -1)

            while int(ay) == int((y + y + h) / 2):
                start_time = time.time()
                break

            while int(ay) <= int((y + y + h) / 2):
                if int(by) <= int((y + y + h) / 2) & int(by + 10) >= int((y + y + h) / 2):
                    cv2.line(img, (bx1, by), (bx2, by), (0, 255, 0), 2)
                    Speed = Speed_Cal(time.time() - start_time)
                    if Speed < xy:
                        Speed *= 2

                    print("Vechile Number " + str(i) + " Speed: " + str(Speed))
                    if Speed > 60.00:
                        print("over speed: " + str(Speed))
                        msg = "Vechile Number " + str(i) + " Speed: " + str(Speed)

                        report_send_mail(msg)

                    # print("Car Number " + str(i))
                    i = i + 1
                    cv2.putText(img, "Speed: " + str(Speed) + "KM/H", (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 1,(255, 0, 0), 3)
                    break
                else:
                    cv2.putText(img, "Calcuting", (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                    break

        cv2.imshow('video', img)

        if cv2.waitKey(33) == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
    return redirect(url_for(""))

if __name__ == '__main__':
    app.run(debug=True)
