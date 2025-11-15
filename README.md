# urban-graffiti-analyzer

This repository contains an interactive Python tool designed for the manual selection and classification of graffiti through cropped regions taken directly from digital images. The project is intended for research in urban ethnography, contemporary archaeology, visual analysis, and cultural studies that require structured information extracted from photographs.

FEATURES

-Interactive interface based on OpenCV.
-Area selection through mouse dragging.
-Instant classification using keyboard input.
-Automatic generation of file names for each crop.
-Registration of identifiers and coordinates associated with each crop.
-Final export to an Excel file containing all generated data.
-Independent configuration system via config.json.
-Compatible with Windows, macOS, and Linux.

PROJECT STRUCTURE

The project should be organized as follows:
-etiquetador_grafitis.py: main program file.
-config.json: file containing the necessary execution paths.
-datos_grafitis.csv: file including ID, X/Y coordinates, and photograph name.
-input_images folder: contains the original images.
-output_crops folder: stores the generated crops.

PREREQUISITES

To run the tool correctly, the following are required:
-Python 3.8 or higher.
-Installed dependencies: OpenCV, Pandas, and Pillow.
-A CSV file with the minimum required data.
-A valid configuration file.

INSTALLATION

-Download or clone the repository into a local folder.
-Create and activate a virtual environment (optional but recommended).
-Install dependencies using:
-pip install -r requirements.txt
-Verify that the input_images and output_crops folders exist and contain the expected files.
-Configure the paths in the config.json file.

CONFIGURATION

The config.json file must include the necessary paths for the program to access the images, the CSV file, and the folder where the generated crops will be stored. An example configuration is as follows:

{
"input_images": "input_images",
"output_crops": "output_crops",
"input_csv": "datos_grafitis.csv"
}

PROGRAM USAGE

-Run the script from the project root folder using:
python etiquetador_grafitis.py
-Select an area in the image by dragging the mouse.
-Assign a category using the corresponding keys.
-Navigate between images using the indicated controls.
-End the session to generate the Excel file with the crops and metadata.

GENERATED OUTPUT

The program produces:
-An Excel file containing complete information about the crops.
-A set of image files containing each generated crop.

LICENSE

This project is distributed under the MIT license. Users may modify, adapt, and redistribute it as long as the license notice is preserved.

AUTHORSHIP AND ACKNOWLEDGEMENT

The script was developed with the assistance of ChatGPT (OpenAI), using version GPT-5.1. This work may be cited as:
Losilla Martínez, N. (2025). Graffiti tagging tool: interactive tool for visual and spatial analysis. GitHub.
