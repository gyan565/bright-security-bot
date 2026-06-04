# Python का बेस वर्ज़न लें
FROM python:3.10.9-slim

# वर्किंग डायरेक्टरी सेट करें
WORKDIR /app

# GitHub की सारी फाइलें कंटेनर में कॉपी करें
COPY . /app

# बोट की ज़रूरी लाइब्रेरीज़ (requirements) इंस्टॉल करें
RUN pip install --no-cache-dir -r requirements.txt

# पोर्ट एक्सपोज़ करें (डमी सर्वर के लिए)
EXPOSE 8080

# बोट को रन करने की कमांड
CMD ["python", "main.py"]
