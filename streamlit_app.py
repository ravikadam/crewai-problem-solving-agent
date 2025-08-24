import streamlit as st
import sys
import os
from pathlib import Path
from io import BytesIO
import tempfile
from datetime import datetime
import markdown
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Streamlit page for mobile responsiveness
st.set_page_config(
    page_title="CrewAI Problem Solver",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add the src directory to the Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from problem_solving_research_agent.crew import ProblemSolvingResearchAgentCrew

# Custom CSS for mobile responsiveness
st.markdown("""
<style>
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }
    
    .stTextInput > div > div > input {
        font-size: 16px;
    }
    
    .stTextArea > div > div > textarea {
        font-size: 16px;
    }
    
    .stButton > button {
        width: 100%;
        font-size: 16px;
        padding: 0.5rem 1rem;
    }
    
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 0.5rem;
            padding-right: 0.5rem;
        }
        
        .stColumns > div {
            padding: 0 0.25rem;
        }
    }
    
    .problem-input {
        font-size: 16px !important;
    }
    
    .result-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def markdown_to_pdf(markdown_content, filename):
    """Convert markdown content to PDF"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Convert markdown to HTML
    html = markdown.markdown(markdown_content)
    soup = BeautifulSoup(html, 'html.parser')
    
    # Process HTML elements
    for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'li']):
        if element.name.startswith('h'):
            # Headers
            level = int(element.name[1])
            if level == 1:
                style = styles['Title']
            elif level == 2:
                style = styles['Heading1']
            elif level == 3:
                style = styles['Heading2']
            else:
                style = styles['Heading3']
            story.append(Paragraph(element.get_text(), style))
            story.append(Spacer(1, 12))
        elif element.name == 'p':
            # Paragraphs
            story.append(Paragraph(element.get_text(), styles['Normal']))
            story.append(Spacer(1, 12))
        elif element.name in ['ul', 'ol']:
            # Lists
            for li in element.find_all('li'):
                story.append(Paragraph(f"• {li.get_text()}", styles['Normal']))
            story.append(Spacer(1, 12))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def run_crewai_workflow(problem_statement):
    """Run the CrewAI workflow and return the result"""
    try:
        inputs = {'problem_statement': problem_statement}
        crew = ProblemSolvingResearchAgentCrew().crew()
        result = crew.kickoff(inputs=inputs)
        return str(result)
    except Exception as e:
        return f"Error running CrewAI workflow: {str(e)}"

def main():
    # Header with mobile-friendly layout
    st.title("🤖 CrewAI Problem Solver")
    st.markdown("**AI-powered research and solution generation**")
    st.markdown("---")
    
    # Mobile-responsive layout
    if st.sidebar.button("ℹ️ Show Instructions"):
        st.info("""
        **How to use:**
        1. Enter your problem statement below
        2. Click 'Generate Solution' 
        3. Wait for AI analysis
        4. Download your PDF report
        """)
    
    # Single column layout for mobile
    st.header("💭 What problem would you like to solve?")
    problem_statement = st.text_area(
        "",
        height=120,
        placeholder="Example: How to build a scalable microservices architecture for an e-commerce platform?",
        key="problem_input",
        help="Describe your problem in detail for better AI analysis"
    )
    
    # Full-width button
    generate_button = st.button(
        "🚀 Generate AI Solution", 
        type="primary",
        use_container_width=True
    )
    
    # Status section
    if generate_button or 'processing' in st.session_state:
        st.markdown("### 📊 Processing Status")
        status_placeholder = st.empty()
        progress_bar = st.progress(0)
    
    # Process the request
    if generate_button and problem_statement.strip():
        st.session_state.processing = True
        
        with status_placeholder.container():
            st.info("🔄 Initializing CrewAI agents...")
            progress_bar.progress(10)
            
            st.info("🔍 Research Specialist analyzing problem...")
            progress_bar.progress(30)
            
            # Run CrewAI workflow
            result = run_crewai_workflow(problem_statement.strip())
            progress_bar.progress(70)
            
            st.info("📄 Document Publisher formatting results...")
            progress_bar.progress(90)
            
            # Generate PDF
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"CrewAI_Solution_{timestamp}.pdf"
            
            try:
                pdf_buffer = markdown_to_pdf(result, filename)
                progress_bar.progress(100)
                
                st.success("✅ Solution generated successfully!")
                
                # Mobile-friendly results display
                st.markdown("---")
                st.markdown("### 📋 Your AI-Generated Solution")
                
                # Compact preview with mobile-friendly styling
                with st.container():
                    st.markdown('<div class="result-container">', unsafe_allow_html=True)
                    
                    # Collapsible preview for mobile
                    with st.expander("📖 View Full Solution", expanded=True):
                        st.markdown(result)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Mobile-friendly download section
                st.markdown("### 📥 Download Options")
                col1, col2 = st.columns(2)
                
                with col1:
                    # PDF Download
                    st.download_button(
                        label="📄 Download PDF",
                        data=pdf_buffer.getvalue(),
                        file_name=filename,
                        mime="application/pdf",
                        use_container_width=True
                    )
                
                with col2:
                    # Text Download
                    st.download_button(
                        label="📝 Download Text",
                        data=result,
                        file_name=f"CrewAI_Solution_{timestamp}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                
            except Exception as e:
                st.error(f"❌ Error generating PDF: {str(e)}")
                
                # Fallback: show text result and offer markdown download
                st.markdown("---")
                st.header("📊 Generated Solution (Text)")
                st.markdown(result)
                
                # Offer markdown download as fallback
                st.download_button(
                    label="📥 Download as Markdown",
                    data=result,
                    file_name=f"CrewAI_Solution_{timestamp}.md",
                    mime="text/markdown"
                )
    
    elif generate_button and not problem_statement.strip():
        st.warning("⚠️ Please enter a problem statement before generating a solution.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>Powered by CrewAI Framework | Built with Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
