# **Adaptive Drone-Based Person Detection Web App 🚀**

This is a **real-time person detection web application** that uses **YOLO for object detection** and **Facial Recognition for unique person tracking**. The model dynamically adjusts processing based on system power levels and ensures **accurate person counting** without false duplicates.

---

## 📌 **Features**
✅ **Live Person Detection** – Detects people in a real-time webcam feed.  
✅ **Unique Person Tracking** – Uses face recognition to avoid duplicate counting.  
✅ **Power Adaptive Processing** – Adjusts model complexity based on system resources.  
✅ **FastAPI Backend** – Lightweight API for handling video streaming.  

---

## 🛠 **Installation Guide**

###  **1.   Clone the Repository**
```bash
git clone 
cd drone-person-detection
```
### **2.    Navigate to the Backend**
```bash
cd backend
```
###  **3.   Install Dependencies**
Ensure you have Python 3.10+ installed. Then, install required packages:
```bash
pip install -r requirements.txt
```
### **4.  Run the Web App**
Start the FastAPI server using Uvicorn:
```bash
uvicorn app:app --reload
```
### **5.  Navigate to the Frontend**
Navigate to frontend folder:
```bash
cd ..
cd frontend
```
### **5.  Run the Web App**
Navigate the React Server:
```bash
npm start
```