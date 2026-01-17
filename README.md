# ☁️ CloudLens: Smart Image Auditor

**A Serverless App that uses AI to "read" your photos.**
LINK:- whttps://d6rq0nk83y8qw.cloudfront.net/

## 🧐 What is this?
This is a web app where you upload an image, and **Artificial Intelligence (AI)** automatically tells you what is inside it (like "Cat", "Car", or "Tree"). It also saves the details and sends you an email alert immediately.

I built this using **AWS Cloud** services, so it runs without any servers!

---

## ⚙️ How It Works (The Flow)
1.  **Upload:** You upload a photo on the website.
2.  **Storage:** The photo is securely saved in the cloud (**S3**).
3.  **AI Scan:** AWS automatically detects the new photo and scans it using **Amazon Rekognition**.
4.  **Save Data:** It extracts the labels (e.g., "Dog, 99% confidence") and saves them in a database (**DynamoDB**).
5.  **Alert:** You get an **Email** instantly with the results.

---

## 🛠️ Tech Stack (Tools Used)
* **Frontend:** HTML, CSS, JavaScript (Hosted on S3 & CloudFront).
* **Backend Code:** AWS Lambda (Python).
* **Storage:** Amazon S3.
* **Database:** Amazon DynamoDB.
* **AI Engine:** Amazon Rekognition.
* **Notifications:** Amazon SNS.

---

## 🚀 Key Features
* ✅ **Zero Servers:** No servers to manage or pay for when idle.
* ✅ **AI Powered:** Uses Machine Learning without training models.
* ✅ **Event-Driven:** Everything happens automatically when a file is uploaded.
* ✅ **Secure:** Protected uploads and access controls.
