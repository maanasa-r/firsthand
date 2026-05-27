# FirstHand 🖥️👋
> **Your personal ASL tutor powered by AI.**

FirstHand is an interactive web application designed to help users learn American Sign Language (ASL) in real-time. By leveraging computer vision and generative AI feedback, it acts as a patient, live human tutor—instantly evaluating hand signs and offering constructive coaching.

---

## 🚀 Key Features

* **Full-Screen Live Feed:** An immersive, clean UI where the entire screen is dedicated to your front-facing webcam.
* **AI-Guided Prompting:** A minimalist prompt box (inspired by Google Gemini) allows users to input any letter, word, or phrase they want to learn.
* **Smart Reference Overlays:** Sleek glassmorphism cards tint dynamically to guide your learning journey visually.
* **Continuous Feedback Loop:** The app listens, watches, and guides you dynamically until your sign is perfect.

---

## ⚙️ How It Works (The User Journey)

### 1. Set the Stage
When you open FirstHand, the interface displays a live, full-screen view of your front-facing web camera. At the bottom-middle sits a clean, modern prompt box equipped with a text area and submit button.

### 2. Choose Your Lesson
Enter any ASL learning prompt (a specific letter, word, or phrase). Instantly, a **red-tinted glass card** appears layered over the top-right of your video feed, showcasing the correct visual representation of the sign you need to make.

### 3. Real-Time Vision Processing
As you attempt the sign, the application processes your webcam feed using advanced computer vision models. It evaluates the gesture against perfect ASL criteria by looking closely at three pillars:
* **Hand Shape:** Are your fingers tucked or extended correctly?
* **Orientation:** Is your palm facing the right direction?
* **Movement:** Are your hands traveling through the air along the proper path?

### 4. Friendly Coaching Feedback
FirstHand avoids frustrating "Wrong, try again" loop messages. Instead, it breaks down its analysis into two intuitive elements:
* **What it saw:** *"It looks like you are trying to sign the letter A."*
* **How to fix it:** *"You're close! Just tuck your thumb a little closer to your hand and make sure your palm faces directly forward."*

### 5. Success Validation
Make the necessary adjustments and try again! As soon as your pose aligns with correct ASL syntax, the glass reference card transitions to a **vibrant light green**, displaying a success message before returning you smoothly to the main prompt screen for your next lesson.

---

## 🛠️ Technology & Models
* **ASL Detection:** Powered by the [Shivakumar ASL American Sign Language Model on Roboflow](https://universe.roboflow.com/shivakumar/asl-american-sign-language/model/1).
* **AI Brain:** Integrated via Python (`google-genai` / `inference`) for parsing conversational, tutor-like feedback.
* **Backend Framework:** Python Flask application (`app.py`).
