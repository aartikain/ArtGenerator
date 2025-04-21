import streamlit as st
import openai
import requests
import io
import base64
from PIL import Image
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Mandala Art Generator",
    page_icon="🔮",
    layout="centered"
)


# App title and description
st.title("Mandala Art Generator")
st.write("Create beautiful mandala art using AI! Customize your mandala with various inspiration elements.")

# Function to generate mandala art using DALLE-3
def generate_mandala(api_key, theme, colors, style, elements, complexity):
    try:
        # Initialize OpenAI client with API key
        client = openai.OpenAI(api_key=api_key)
        
        # Create a detailed prompt incorporating all user inputs
        mandala_prompt = f"""Create a beautiful and intricate mandala art design with the following characteristics:
- Central theme: {theme}
- Color scheme: {colors}
- Art style: {style}
- Special elements to incorporate: {elements}
- Complexity level: {complexity}
- Perfect radial symmetry from the center
- Highly detailed patterns and ornate designs
- Sacred geometry elements incorporated into the design
- The entire image should be the mandala with no text or border"""
        
        # Generate the image using DALLE-3
        response = client.images.generate(
            model="dall-e-3",
            prompt=mandala_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        # Get the image URL from the response
        image_url = response.data[0].url
        
        # Download the image
        img_data = requests.get(image_url).content
        img = Image.open(io.BytesIO(img_data))
        
        return img, image_url
    
    except Exception as e:
        st.error(f"Error generating image: {str(e)}")
        return None, None

# Function to get a download link for the image
def get_image_download_link(img, filename, text):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{img_str}" download="{filename}">📥 {text}</a>'
    return href

# Create form for user inputs with multiple customization options
with st.form("mandala_form"):
    # Main theme input
    theme = st.text_input("Main Theme/Inspiration (required)", 
                         placeholder="e.g., ocean waves, lotus flower, cosmos")
    
    # Color scheme selection
    color_options = [
        "Vibrant and colorful",
        "Pastel colors",
        "Earth tones",
        "Ocean blues",
        "Galaxy purples and blues",
        "Golden and royal",
        "Black and white",
        "Monochromatic",
        "Custom color scheme"
    ]
    colors = st.selectbox("Color Scheme", color_options)
    
    # If custom colors are selected
    if colors == "Custom color scheme":
        colors = st.text_input("Enter your custom color scheme", 
                              placeholder="e.g., teal, gold, and purple")
    
    # Art style dropdown
    style_options = [
        "Traditional mandala",
        "Modern geometric",
        "Floral and organic",
        "Abstract",
        "Celestial/cosmic",
        "Tribal/ethnic",
        "Psychedelic",
        "Minimalist"
    ]
    style = st.selectbox("Art Style", style_options)
    
    # Special elements multiselect
    element_options = [
        "Animals or creatures",
        "Plants and flowers",
        "Crystals and gems",
        "Sacred symbols",
        "Celestial bodies",
        "Water elements",
        "Fire elements",
        "Geometric patterns"
    ]
    elements = st.multiselect("Special Elements to Include (optional)", element_options)
    elements_str = ", ".join(elements) if elements else "None"
    
    # Complexity level
    complexity_options = [
        "Simple and elegant",
        "Moderately detailed",
        "Highly intricate and complex"
    ]
    complexity = st.select_slider("Complexity Level", complexity_options)
    
    # API key input with a password field for security
    api_key = st.text_input("Enter your OpenAI API key (required)", 
                           type="password", 
                           help="Your OpenAI API key is required to use DALLE-3")
    
    # Submit button
    submitted = st.form_submit_button("Generate Mandala")

# Process form submission
if submitted:
    # Validate inputs
    if not theme:
        st.error("Please enter a main theme or inspiration for your mandala.")
    elif not api_key:
        st.error("Please enter your OpenAI API key.")
    else:
        # Show loading message
        with st.spinner("Generating your mandala art... This may take up to 30 seconds."):
            # Generate the mandala
            mandala_image, image_url = generate_mandala(api_key, theme, colors, style, elements_str, complexity)
            
            if mandala_image:
                # Display the generated image
                st.success("Your mandala art has been created!")
                st.image(mandala_image, caption=f"Mandala inspired by: {theme}", use_column_width=True)
                
                # Display the customization details
                with st.expander("View Customization Details"):
                    st.write(f"**Theme:** {theme}")
                    st.write(f"**Color Scheme:** {colors}")
                    st.write(f"**Art Style:** {style}")
                    st.write(f"**Special Elements:** {elements_str}")
                    st.write(f"**Complexity:** {complexity}")
                
                # Create a download link
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"mandala_{timestamp}.png"
                st.markdown(get_image_download_link(mandala_image, filename, "Download Your Mandala"), unsafe_allow_html=True)
                
                # Display a tip
                st.info("💡 Tip: Try different combinations of theme, colors, and elements to create unique mandala designs!")

# Add some helpful information at the bottom
st.markdown("---")
st.markdown("""
### About This App
This app uses OpenAI's DALLE-3 model to generate unique mandala art based on your customizations. 
The generation process may take up to 30 seconds depending on OpenAI's processing time.

### Note
- You'll need your own OpenAI API key to use this app
- Each generation will count against your OpenAI API usage
- Experiment with different combinations for unique results
""")

# Footer
st.markdown("---")
st.markdown("Created with ❤️ using Python 3, Streamlit and OpenAI DALLE-3")
