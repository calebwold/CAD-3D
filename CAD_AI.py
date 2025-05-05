import streamlit as st
from openai import OpenAI
import subprocess
import uuid
import tempfile
import os
import pyvista as pv
from stpyvista import stpyvista
import streamlit.components.v1 as components
import base64
import trimesh

client = OpenAI(
    api_key="api key goes here"  # Your API key
)

# Set the page configuration
st.set_page_config(layout="wide", page_title="3D ")

def file_to_base64_string(file_path):
    """
    Converts a file to a Base64 encoded string.
    """
    with open(file_path, 'rb') as file:
        encoded_string = base64.b64encode(file.read()).decode('utf-8')
    return encoded_string
## Function to render STL files using PyVista
def render_stl_with_pyvista(stl_file_path):
    """
    Renders an STL file using PyVista.
    """
    plotter = pv.Plotter(window_size=[400, 400])
    mesh = pv.read(stl_file_path)
    plotter.add_mesh(mesh, show_edges=True, edge_color="black")
    plotter.background_color = "white"
    plotter.view_isometric()
    return plotter
## Function to convert OpenSCAD code to STL
def convert_openscad_code_to_stl(code_str, output_filename, format_type="stl"):
    """
    Converts OpenSCAD code to an STL file.
    """
    output_path = os.path.join(os.getcwd(), output_filename)
    # Create a temporary file to store the OpenSCAD code
    with tempfile.NamedTemporaryFile(delete=False, suffix='.scad', mode='w', dir=os.getcwd()) as tmp_file:
        tmp_file_name = tmp_file.name
        tmp_file.write(code_str)
    
    command = ['openscad', '-o', output_path, '--export-format', format_type, tmp_file_name]
    # Check if OpenSCAD is installed
    try:
        subprocess.run(command, check=True)
        st.success(f"Conversion successful. File saved to: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        st.error(f"Error during conversion: {e}")
        return False
    finally:
        os.remove(tmp_file_name)
## Function to convert STL to GLB
def stl_to_glb(stl_file_path, glb_file_path):
    """
    Converts an STL file to a GLB file using Trimesh.
    """
    try:
        mesh = trimesh.load(stl_file_path)
        mesh.export(glb_file_path, file_type='glb')
        return True
    except Exception as e:
        st.error(f"Error converting STL to GLB: {e}")
        return False
## Function to query GPT-4 for OpenSCAD code generation
def query_gpt4(prompt):
    """
    Queries GPT-4 for OpenSCAD code generation.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional in OPENSCAD and create openscad code for people's prototypes. Generate only the code without any explanations or markdown that can be made for 2d or 3d drawings which will always prodce a solid output which matches the description."},
                {"role": "user", "content": f"Generate the OPENSCAD code for the following idea, only return your openscad code and nothing else whatsoever: {prompt}"}
            ]
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error querying OpenAI: {e}")
        return None

def display_3d_model(glb_file_path, stl_file_path):
    """
    Displays a 3D model using model-viewer.
    """
    try:
        glb_base64 = file_to_base64_string(glb_file_path)

        placeholder_image = "https://placehold.co/600x400/gray/white?text=Loading+3D+Model"
        
        components.html(
            f'''
            <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.4.0/model-viewer.min.js"></script>
            <model-viewer 
                style="width: 100%; height: 600px;" 
                src="data:model/gltf-binary;base64,{glb_base64}" 
                poster="{placeholder_image}" 
                tone-mapping="commerce" 
                shadow-intensity="2" 
                camera-controls 
                touch-action="pan-y" 
                alt="3D Render" 
                skybox-image="https://upload.wikimedia.org/wikipedia/commons/1/18/Sunset_hdr.jpg">
            </model-viewer>
            ''',
            height=650,
            width=None
        )
        
        try:
            with open(stl_file_path, "rb") as file:
                file_bytes = file.read()
                st.download_button(
                    label="Download STL File",
                    data=file_bytes,
                    file_name=os.path.basename(stl_file_path),
                    mime="application/octet-stream"
                )
        except Exception as e:
            st.error(f"Error preparing download: {e}")
    except Exception as e:
        st.error(f"Error displaying 3D model: {e}")

def main():
    st.title("3D Model Generator")
    st.write("Enter a description of the 3D model you want to create, and the AI will generate OpenSCAD code for it.")
    
    with st.expander("Examples", expanded=False):
        st.markdown("""
        - A simple coffee mug with handle
        - A phone stand with adjustable angle
        - A geometric vase with hexagonal pattern
        - A miniature chess piece (knight)
        - A desk organizer with compartments
        """)
    
    userInput = st.text_area("Enter your prompt here", height=100, 
                           placeholder="Example: A simple phone stand with a 45-degree angle")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        generate_btn = st.button("Generate 3D Model", type="primary", use_container_width=True)
    
    # Check if OpenSCAD is installed outside the button click
    openscad_installed = False
    try:
        subprocess.run(['openscad', '--version'], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE, 
                      check=False, 
                      text=True)
        openscad_installed = True
    except FileNotFoundError:
        st.warning("⚠️ OpenSCAD not found. You'll need to install it for 3D model generation.")
        st.info("Download OpenSCAD from: https://openscad.org/downloads.html")
    
    if generate_btn and userInput:
        with st.spinner("Generating OpenSCAD code..."):
            openScadCode = query_gpt4(userInput)
            
        if openScadCode:
            st.subheader("Generated OpenSCAD Code")
            st.code(openScadCode, language="openscad")
            
            # If OpenSCAD is not installed, provide a way to save the code
            if not openscad_installed:
                st.download_button(
                    label="Download OpenSCAD Code",
                    data=openScadCode,
                    file_name="model.scad",
                    mime="text/plain"
                )
                st.warning("OpenSCAD is not installed, so STL generation is not available. Please install OpenSCAD and try again.")
            else:
                with st.spinner("Converting to 3D model..."):
                    fileName = str(uuid.uuid4())
                    filenameStl = fileName + ".stl"
                    filenameGlb = fileName + ".glb"
                    
                    if convert_openscad_code_to_stl(openScadCode, filenameStl, "stl"):
                        st.success("STL file generated successfully!")
                        
                        try:
                            if stl_to_glb(filenameStl, filenameGlb):
                                st.success("GLB file generated successfully!")
                                display_3d_model(filenameGlb, filenameStl)
                                
                                # Offer to show PyVista visualization
                                with col2:
                                    if st.button("Show Alternative 3D View", use_container_width=True):
                                        st.write("PyVista Visualization:")
                                        try:
                                            stpyvista(render_stl_with_pyvista(filenameStl))
                                        except Exception as e:
                                            st.error(f"Error rendering with PyVista: {e}")
                        except Exception as e:
                            st.error(f"Error converting to GLB or displaying model: {e}")
                            
                            # Offer STL download even if GLB conversion fails
                            if os.path.exists(filenameStl):
                                try:
                                    with open(filenameStl, "rb") as file:
                                        file_bytes = file.read()
                                        st.download_button(
                                            label="Download STL File",
                                            data=file_bytes,
                                            file_name=filenameStl,
                                            mime="application/octet-stream"
                                        )
                                except Exception as download_error:
                                    st.error(f"Error preparing download: {download_error}")
    
    st.sidebar.header("About")
    st.sidebar.write("""
    This app uses OpenAI's GPT-4o-mini to generate OpenSCAD code from your text descriptions.
    The code is then converted to a 3D model that you can view and download.
    
    Requirements:
    - OpenSCAD must be installed and accessible in your PATH
    - An OpenAI API key must be configured in the app
    """)
    
    if not openscad_installed:
        st.sidebar.warning("⚠️ OpenSCAD is not installed or not found in your PATH.")
        st.sidebar.markdown("""
        ### Installing OpenSCAD
        
        1. Download from: [openscad.org](https://openscad.org/downloads.html)
        2. Run the installer
        3. Make sure OpenSCAD is added to your PATH
        4. Restart this app
        """)
    
    st.sidebar.info("Note: This is a demo application and may have limitations.")

if __name__ == "__main__":
    main()
