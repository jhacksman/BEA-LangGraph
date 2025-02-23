"""
Streamlit UI for document processing workflow.

This module provides a web interface for:
- Document upload and input
- Processing criteria specification
- Interactive Q&A
- Result downloading
"""

import streamlit as st
import tempfile
from pathlib import Path
from typing import List, Optional

from agents.basic_workflow import DocumentWorkflow, WorkflowConfig
from agents.basic_workflow.api.client import VeniceClient

def save_uploadedfile(uploaded_file) -> Optional[Path]:
    """Save uploaded file to temp directory."""
    if uploaded_file is None:
        return None
        
    with tempfile.NamedTemporaryFile(delete=False, suffix='.md') as tmp:
        tmp.write(uploaded_file.getvalue())
        return Path(tmp.name)

def main():
    st.title("Document Processing Workflow")
    
    # Initialize session state
    if "workflow" not in st.session_state:
        api_key = st.secrets.get("VENICE_API_KEY", "B9Y68yQgatQw8wmpmnIMYcGip1phCt-43CS0OktZU6")
        client = VeniceClient(api_key)
        st.session_state.client = client
    
    # Document input section
    st.header("Document Input")
    input_type = st.radio("Input Type", ["Upload File", "Enter Text"])
    
    document_content = ""
    if input_type == "Upload File":
        uploaded_file = st.file_uploader("Upload Document", type=["txt", "md"])
        if uploaded_file:
            document_content = uploaded_file.getvalue().decode()
    else:
        document_content = st.text_area("Enter Document Content")
    
    # Criteria input
    st.header("Processing Criteria")
    criteria = st.text_area("Enter criteria (one per line)")
    criteria_list = [c.strip() for c in criteria.split("\n") if c.strip()]
    
    # Configuration
    st.header("Workflow Configuration")
    max_revisions = st.slider("Maximum Revisions", 1, 5, 3)
    require_approval = st.checkbox("Require Approval", value=True)
    
    if st.button("Process Document"):
        if not document_content:
            st.error("Please provide document content")
            return
            
        if not criteria_list:
            st.error("Please provide at least one criterion")
            return
        
        # Create workflow configuration
        config = WorkflowConfig(
            criteria=criteria_list,
            max_revisions=max_revisions,
            require_approval=require_approval
        )
        
        # Initialize workflow
        workflow = DocumentWorkflow(config, st.session_state.client)
        
        # Process document with progress bar
        with st.spinner("Processing document..."):
            try:
                result = await workflow.run({
                    "document": DocumentState(content=document_content),
                    "config": config
                })
                
                # Display results
                st.header("Results")
                
                # Show final document
                st.subheader("Final Document")
                st.markdown(result["document"].content)
                
                # Show revision history
                if result["document"].revision_history:
                    st.subheader("Revision History")
                    for i, revision in enumerate(result["document"].revision_history, 1):
                        with st.expander(f"Revision {i}"):
                            st.markdown(revision)
                
                # Show review feedback
                if result["document"].review_feedback:
                    st.subheader("Review Feedback")
                    for i, feedback in enumerate(result["document"].review_feedback, 1):
                        with st.expander(f"Feedback {i}"):
                            st.markdown(feedback)
                
                # Download button
                st.download_button(
                    "Download Result",
                    result["document"].content,
                    file_name="processed_document.md",
                    mime="text/markdown"
                )
                
            except Exception as e:
                st.error(f"Error processing document: {str(e)}")

if __name__ == "__main__":
    main()
