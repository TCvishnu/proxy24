# Multiplayer Speed Typing and Quiz Game

Welcome to the **Multiplayer Speed Typing and Quiz Game**, a fun and interactive command-line competition designed to challenge your typing speed and knowledge. This project combines a traditional speed typing game with a quiz component, allowing players to race against each other while also answering topic-based questions for extra points—all in real-time!

## Features

- **Multiplayer Speed Typing**: Compete against others to type a given passage as fast and accurately as possible.
- **Quiz Mode**: Answer questions on a topic of your choice during the typing race to earn extra points. Correct answers increase your score!
- **Real-time Feedback**: Receive live updates on your typing progress (words per minute and accuracy) as you play.
- **Dynamic Leaderboard**: Rankings based on typing speed, accuracy, and quiz performance.

## Tools & Technologies Used

- **Python**: The entire game is developed using Python, leveraging its simplicity and powerful libraries for network communication and user interface.
  
- **npyscreen**: For creating the command-line user interface (CLI), we used `npyscreen`, which makes it easy to build text-based interfaces. It allowed us to design input forms, real-time display of results, and smooth navigation—all while keeping the game fully within the terminal.

- **Firebase**: Player data, including scores and game stats, are stored and managed using Firebase’s real-time database. Firebase ensures that game results are synced efficiently, even when multiple players are competing at once.

- **Socket Programming**: Python’s `socket` module is used to manage communication between the server and multiple players. This enables the real-time multiplayer experience.

## Getting Started

### Prerequisites

To run the project, you'll need to install a few dependencies:

1. **Python 3.x**: Ensure you have Python installed. You can download it from [here](https://www.python.org/downloads/).
2. **Firebase SDK**: Install Firebase Admin SDK for Python.
   ```bash
   pip install firebase-admin
3. **npyscreen:** Install the npyscreen library for building command-line UIs
   ```bash
   pip install npyscreen

## Installation Instructions

To set up the project and install the required dependencies, follow these steps:

### Prerequisites

Make sure you have Python 3.x installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### Clone the Repository

1. **Clone the repository**:
   ```bash
   git clone https://github.com/TCvishnu/proxy24.git

2. **Start playing the game**:
  ```bash
    python center.py
```

## Contributors

- **Vishnu TC**
- **K. Govind**
- **Abhinand Nandakumar**
- **Shreya Jayaraj**


