# Group Repository for the Data Science Mini-Project (EMATM0050)

# Python Environment Setup Guide

Follow these steps to set up your Python environment for this project.

---

## Prerequisites

- Ensure you have **Python 3.12 +** installed on your system. ( I was running the code on python 3.12.7 )

---

## Steps to Set Up the Environment

1. **Create a Virtual Environment**:
   ```bash
   python -m venv <env_name>

Replace <env_name> with the desired name for your environment.

Note: Keep the environment folder out of your Git repository to avoid committing it.

2. **Activate the Virtual Environment**:
On macOS/Linux:
  ```bash
  source <env_name>/bin/activate
  ```

On Windows:
```bash
    .\<env_name>\Scripts\activate
```

Install Dependencies: Use the requirements.txt file to install the necessary packages:

```bash
pip install -r requirements.txt
```

**Important: Do not modify the version numbers in requirements.txt.**

Deactivate the Environment: If you need to deactivate the environment, run:

```bash
deactivate
```

Group Number: T3

Problem Assigned: Sapienza (F)

Group Members: Shaivya Shankar, Pulkit Dhingra, Luoxi Liu, Shuyi Li
