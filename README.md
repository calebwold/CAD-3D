# CAD-3D
CAD 3D
# 3D Model Generator with Streamlit and OpenAI

This application allows users to generate 3D models from textual descriptions using **Streamlit** for the interface, **OpenAI GPT-4o-mini** to generate **OpenSCAD** code, and **OpenSCAD** to convert the code into 3D models. The app supports **STL** and **GLB** file exports for 3D viewing and interaction.

---

## Features

- **Text-to-3D Model Generation**: Generate 3D models from text descriptions using OpenAI's GPT-4o-mini.
- **3D Model Viewer**: View the generated model in 3D in your browser.
- **STL & GLB File Export**: Download the generated models as STL or GLB files.
- **PyVista Alternative Visualization**: View the STL file using PyVista for additional 3D visualization.

---

## Requirements

Before using this app, you'll need to install a few dependencies. Follow these steps to get everything set up.

### Step 1: Install Python and Virtual Environment

First, make sure **Python 3.8+** is installed on your system. You can download Python from the official site:

- [Download Python](https://www.python.org/downloads/)

To verify Python is installed, open a terminal or command prompt and run:

```bash
python --version
If Python is not installed, follow the instructions on the website to install it. Make sure to add Python to your PATH during installation.

Next, create a virtual environment to manage dependencies:

bash
Copy
Edit
python -m venv venv
Activate the virtual environment:

On Windows:

bash
Copy
Edit
venv\Scripts\activate
On macOS/Linux:

bash
Copy
Edit
source venv/bin/activate
Step 2: Install Python Dependencies
With the virtual environment activated, install all the required Python libraries by running:

bash
Copy
Edit
pip install -r requirements.txt
The requirements.txt file contains these dependencies:

txt
Copy
Edit
streamlit
openai
pyvista
stpyvista
trimesh
python-dotenv
This will install all the necessary libraries for running the app.

Step 3: Install OpenSCAD
OpenSCAD is used to generate 3D models from OpenSCAD code. Follow these steps to install it:

Download OpenSCAD:

Go to OpenSCAD Downloads and download the installer for your operating system.

Select the appropriate version based on your system (Windows, macOS, or Linux).

Install OpenSCAD:

Windows: Run the installer and follow the prompts. During installation, ensure the box to add OpenSCAD to your system’s PATH is checked.

macOS: Open the downloaded .dmg file and drag OpenSCAD to the Applications folder.

Linux: Follow the instructions specific to your distribution. For example, on Ubuntu, run:

bash
Copy
Edit
sudo apt-get install openscad
Verify OpenSCAD Installation:
After installation, you need to confirm that OpenSCAD is installed correctly. Open a terminal or command prompt and run:

bash
Copy
Edit
openscad --version
This should output the version of OpenSCAD installed. If it doesn’t work, ensure that OpenSCAD is correctly added to your system’s PATH.

Step 4: Set Up OpenAI API Key
The app uses OpenAI GPT-4o-mini to generate OpenSCAD code from your text descriptions. You need an OpenAI API key for this.

Sign up or log in to OpenAI at OpenAI API.

Get your API key from the API keys section.

Create a .env file in the root directory of your project (same directory as this README), and add your API key as follows:

ini
Copy
Edit
OPENAI_API_KEY=your_openai_api_key_here
Step 5: Run the Application
Once you have installed all dependencies and set up OpenSCAD and your OpenAI API key, you can run the app:

Run Streamlit: In the terminal, navigate to the directory where the app’s app.py file is located and run the following command:

bash
Copy
Edit
streamlit run app.py
This will start a local web server, and you should see an output similar to this:

nginx
Copy
Edit
You can now view your Streamlit app in your browser.

Local URL:  http://localhost:8501
Network URL: http://<your-ip>:8501
Open the app in your browser: Go to http://localhost:8501 in your web browser to use the app.

How the App Works
Enter a description: Provide a description of the 3D model you want to create.

Generate OpenSCAD Code: The app will use GPT-4o-mini to generate OpenSCAD code based on the description.

Convert to 3D Models: The OpenSCAD code is converted to STL and GLB files.

View & Download: You can view the generated 3D model in the browser and download the STL/GLB files.

Example Prompts
You can use the following example prompts to test the app:

A simple coffee mug with handle

A phone stand with adjustable angle

A geometric vase with hexagonal pattern

A miniature chess piece (knight)

A desk organizer with compartments

Troubleshooting
OpenSCAD not found: If OpenSCAD is not found or not added to the PATH, ensure you’ve installed OpenSCAD and followed the instructions to add it to your PATH.

API key issues: Make sure you’ve created and added your OpenAI API key correctly in the .env file.

Error generating models: If there's an issue generating the model, verify OpenSCAD is installed and accessible by the app.

About
This app is powered by:

Streamlit for the web interface

OpenAI GPT-4o-mini for generating OpenSCAD code from text descriptions

PyVista for alternative 3D visualization

Trimesh for STL to GLB conversion

License
This project is licensed under the MIT License - see the LICENSE file for details.

vbnet
Copy
Edit

### Key Updates for Complete Installation:
1. **Python Setup**: Instructions to install Python, create a virtual environment, and install required dependencies.
2. **Detailed OpenSCAD Installation**: Complete steps on how to install OpenSCAD on all major operating systems (Windows, macOS, and Linux).
3. **API Key Setup**: Clear steps for setting up the OpenAI API key.
4. **Running the Application**: Instructions on running the app with Streamlit, including expected output.
