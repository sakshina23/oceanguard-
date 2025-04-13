from flask import Flask, render_template, request, send_file
import os
import joblib
import cv2
import numpy as np
import datetime
import csv
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("⚠️ Warning: GEMINI_API_KEY not found in environment variables")
else:
    genai.configure(api_key=api_key)

try:
    # Initialize Gemini model with the correct name
    gemini_model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
except Exception as e:
    print(f"Error initializing Gemini model: {str(e)}")

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
REPORT_FILE = 'reports/reports.csv'
MODEL_PATH = 'plastic_detector.pkl'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('reports', exist_ok=True)

plastic_model = joblib.load(MODEL_PATH)

def extract_features(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return None
    image = cv2.resize(image, (128, 128))
    hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8],
                        [0, 256, 0, 256, 0, 256]).flatten()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    edge_density = np.sum(edges) / (128 * 128)
    return np.concatenate([hist, [edge_density]])

def send_email_alert(location, filename, latitude=None, longitude=None):
    # Email configuration
    sender = os.getenv('EMAIL_USER', 'sakshina23@gmail.com')
    password = os.getenv('EMAIL_PASSWORD', 'bhpmeacujnikjvao')
    recipient = os.getenv('RECIPIENT_EMAIL', '31240817@vupune.ac.in')

    # Create the email message
    msg = EmailMessage()
    msg['Subject'] = "🚨 Plastic Pollution Alert - OceanGuard"
    msg['From'] = sender
    msg['To'] = recipient

    # Create location link if coordinates are available
    location_link = ""
    if latitude and longitude:
        location_link = f"https://www.google.com/maps?q={latitude},{longitude}"

    # Create informative email body
    body = f"""
Dear Municipal Cleanup Team,

We hope this message finds you well.  
This is an automated alert from the **OceanGuard** environmental monitoring system.

🧴 **Plastic pollution has been detected** in the following location:

📍 **Coordinates**: {latitude}, {longitude}  
📌 **Google Maps Link**:  
{location_link}

🕒 **Timestamp**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
📷 **Image Evidence**: Attached below

We respectfully request a site inspection and cleanup action at the earliest convenience to prevent this plastic waste from entering nearby water bodies.

🌊 Keeping our oceans and rivers clean is a collective responsibility — and we deeply appreciate your support and responsiveness.

Thank you for your service to the environment and the community.

Warm regards,  
**OceanGuard Detection System**  
Email: alerts@oceanguard.com  
Website: https://oceanguard.vercel.app
    """

    # Set the email body first
    msg.set_content(body)

    # Add image attachment
    try:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(image_path, 'rb') as f:
            image_data = f.read()
        msg.add_attachment(image_data, maintype='image', subtype='jpeg', filename=filename)
    except Exception as e:
        print(f"⚠️ Warning: Could not attach image: {str(e)}")

    try:
        # Create SMTP connection with timeout
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)
        print("✅ Email alert sent successfully with image attachment")
        return True
    except smtplib.SMTPAuthenticationError:
        print("❌ Email authentication failed. Please check your email credentials.")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ Email sending failed: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error while sending email: {str(e)}")
        return False

def get_llm_analysis(location, result):
    """
    Get detailed analysis and recommendations from Gemini based on the detection result.
    """
    try:
        if not api_key:
            return "Gemini analysis unavailable - API key not configured"

        if 'gemini_model' not in globals():
            return "Gemini model not properly initialized"

        # Prepare the prompt
        prompt = f"""
        Analyze this plastic pollution detection case:
        - Location: {location}
        - Detection Result: {result}
        
        Please provide:
        1. A detailed analysis of potential environmental impact
        2. Specific cleanup recommendations
        3. Preventive measures for this location
        4. Relevant environmental regulations or guidelines
        
        Format the response in a clear, structured way.
        """
        
        # Generate response with Gemini
        response = gemini_model.generate_content(prompt)
        
        if response and hasattr(response, 'text'):
            return response.text
        else:
            return "Gemini analysis: No valid response generated"
            
    except Exception as e:
        error_msg = str(e)
        print(f"Error getting Gemini analysis: {error_msg}")
        return f"Gemini analysis unavailable. Error: {error_msg}"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/references")
def references():
    return render_template("references.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    return render_template("upload.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    location = request.form["location"]
    result = request.form["result"]
    filename = request.form["filename"]
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")
    
    # Get Gemini analysis
    llm_analysis = get_llm_analysis(location, result)
    
    # Get current timestamp
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return render_template("analysis.html",
                         location=location,
                         result=result,
                         filename=filename,
                         latitude=latitude,
                         longitude=longitude,
                         llm_analysis=llm_analysis,
                         analysis_time=current_time)

@app.route("/submit", methods=["POST"])
def submit():
    file = request.files["image"]
    location = request.form["location"]
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")
    filename = file.filename
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    features = extract_features(filepath)
    if features is None:
        result = "Error processing image"
    else:
        prediction = plastic_model.predict([features])[0]
        result = "Plastic Present" if prediction == 1 else "No Plastic"

    if result == "Plastic Present":
        send_email_alert(location, filename, latitude, longitude)

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    report_row = [now, location, result, filename]
    if latitude and longitude:
        report_row.extend([latitude, longitude])
    
    file_exists = os.path.exists(REPORT_FILE)
    with open(REPORT_FILE, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            headers = ['Timestamp', 'Location', 'Result', 'Filename']
            if latitude and longitude:
                headers.extend(['Latitude', 'Longitude'])
            writer.writerow(headers)
        writer.writerow(report_row)

    return render_template("result.html", 
                         location=location, 
                         result=result, 
                         filename=filename,
                         latitude=latitude,
                         longitude=longitude)

@app.route("/download")
def download():
    return send_file(REPORT_FILE, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
