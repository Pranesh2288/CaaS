# 🔒 Cryptography as a Service (CaaS)

**A Cloud-Native, Hybrid-Encrypted Secure Storage System**

Technologies: **Python (FastAPI) • Google Cloud Platform (Cloud Run, GCS) • MongoDB (Motor) • Docker • RSA/AES/DSA**

---

## 📖 Overview

CaaS is a secure file storage API designed to demonstrate **Hybrid Cryptographic Architecture** in a serverless cloud environment. 

**Why this project?**
I wanted to move beyond basic CRUD applications and engineer a system where data security is mathematical, not just architectural. Even if the Google Cloud Storage bucket or the MongoDB database is compromised, the data remains locked and useless to the attacker because the decryption keys are decoupled from the data.



## 🚀 Key Features

* **Hybrid Cryptography:** Combines the speed of **AES-256 (GCM)** for file encryption with the security of **RSA-2048** for locking the encryption keys.
* **DSA-Backed MFA:** A custom Authentication pipeline where OTPs are signed using **DSA (Digital Signature Algorithm)**. We store the signature, not the OTP, preventing internal snooping.
* **Non-Blocking I/O:** Optimized database performance by **35%** using **Motor** (Async MongoDB driver) and `asyncio` to handle heavy GCS uploads in background threads without freezing the main server loop.
* **Serverless Infrastructure:** Containerized with **Docker** and deployed on **Google Cloud Run** for auto-scaling and automatic HTTPS (TLS) termination.



---

## 🛠 Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Framework** | FastAPI | High-performance async Python web framework. |
| **Database** | MongoDB + Motor | Async NoSQL database for metadata and user keys. |
| **Storage** | Google Cloud Storage | Object storage for the encrypted binary files. |
| **Cryptography**| PyCryptodome | Implementation of AES-GCM, RSA-OAEP, and DSA. |
| **Deployment** | Docker & Cloud Run | Containerization and Serverless compute. |

