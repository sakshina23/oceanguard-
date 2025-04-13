# 🌊 OceanGuard - Plastic Detection System

OceanGuard is an AI-powered web application that helps detect and analyze plastic pollution in images. It combines computer vision and AI to provide detailed analysis and automated alerts for plastic waste detection.

## 🚀 Features

- **Plastic Detection**: Uses machine learning to detect plastic in images
- **AI Analysis**: Provides detailed environmental impact analysis using Gemini AI
- **Automated Alerts**: Sends email notifications when plastic is detected
- **Location Tracking**: Records and maps detection locations
- **Report Generation**: Creates downloadable reports of detections
- **Modern UI**: Beautiful ocean-themed interface with premium design

## 🛠️ Tech Stack

- **Backend**: Python/Flask
- **Frontend**: HTML, CSS, JavaScript
- **ML**: OpenCV, Joblib
- **AI**: Google Gemini API
- **Email**: SMTP
- **Styling**: Modern CSS with glassmorphism

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- Gmail account (for email notifications)

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/oceanguard.git
cd oceanguard
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory:
```env
# LLM Configuration
LLM_TYPE=gemini

# API Keys
GEMINI_API_KEY=your_gemini_api_key_here

# Email configuration
EMAIL_USER=your_gmail@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
RECIPIENT_EMAIL=recipient@example.com
```

5. Get your API keys:
   - Gemini API: Visit https://makersuite.google.com/app/apikey
   - Gmail App Password: Enable 2-Step Verification and generate an App Password

## 🎮 Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Upload an image and provide location details

4. View the detection results and AI analysis

## 📁 Project Structure

```
oceanguard/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables
├── static/               # Static files
│   ├── uploads/         # Uploaded images
│   └── images/          # Website images
├── templates/           # HTML templates
│   ├── home.html       # Landing page
│   ├── upload.html     # Upload form
│   ├── result.html     # Detection results
│   └── analysis.html   # AI analysis
└── reports/             # CSV reports
    └── reports.csv     # Detection history
```

## 🔧 Configuration

- **Email Settings**: Update `.env` with your Gmail credentials
- **API Keys**: Add your Gemini API key in `.env`
- **Model Path**: Ensure `plastic_detector.pkl` is in the root directory

## 📧 Email Setup

1. Enable 2-Step Verification in your Google Account
2. Generate an App Password
3. Use the App Password in your `.env` file

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details

## 🙏 Acknowledgments

- Google Gemini API
- OpenCV
- Flask
- All contributors and supporters

## 📞 Support

For support, email support@oceanguard.com or open an issue in the repository. 