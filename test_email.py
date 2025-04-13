from app import send_email_alert

def test_email():
    print("Testing email functionality...")
    result = send_email_alert("Test Location", "test_image.jpg")
    if result:
        print("Email test successful!")
    else:
        print("Email test failed. Please check the error messages above.")

if __name__ == "__main__":
    test_email() 