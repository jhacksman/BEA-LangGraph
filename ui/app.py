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
import asyncio

from pydantic import BaseModel, Field

from bea_langgraph.agents.basic_workflow.chain import DocumentWorkflow
from bea_langgraph.agents.basic_workflow.models import DocumentState, WorkflowConfig
from bea_langgraph.agents.basic_workflow.api.client import VeniceClient

def save_uploadedfile(uploaded_file) -> Optional[Path]:
    """Save uploaded file to temp directory."""
    if uploaded_file is None:
        return None
        
    with tempfile.NamedTemporaryFile(delete=False, suffix='.md') as tmp:
        tmp.write(uploaded_file.getvalue())
        return Path(tmp.name)

def main():
    try:
        st.set_page_config(page_title="Document Processing Workflow", layout="wide")
    except:
        pass
        
    st.title("Document Processing Workflow")
    
    # Initialize session state
    if "client" not in st.session_state:
        api_key = st.secrets.get("VENICE_API_KEY")
        if not api_key:
            st.error("Venice API key not found in secrets. Please configure it in your Streamlit secrets.")
            return
        client = VeniceClient(api_key)
        st.session_state.client = client
        
    if "processing_state" not in st.session_state:
        st.session_state.processing_state = None
        
    if "document_content" not in st.session_state:
        st.session_state.document_content = ""
        
    if "criteria_list" not in st.session_state:
        st.session_state.criteria_list = []
    
    # Document input section
    st.header("Document Input")
    input_type = st.radio("Input Type", ["Enter Text", "Upload File"], key="input_type", horizontal=True, index=0)
    
    if input_type == "Upload File":
        uploaded_file = st.file_uploader("Upload Document", type=["txt", "md"], key="file_uploader")
        if uploaded_file:
            try:
                content = uploaded_file.getvalue().decode()
                st.session_state.document_content = content
                st.success("File uploaded successfully!")
                with st.expander("Document Preview", expanded=True):
                    st.markdown(content)
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
    else:
        content = st.text_area(
            "Enter Document Content",
            value=st.session_state.document_content,
            key="doc_content",
            height=200,
            placeholder="Enter your document content here..."
        )
        st.session_state.document_content = content
        if content:
            with st.expander("Document Preview", expanded=True):
                st.markdown(content)
    
    # Show document preview
    if st.session_state.document_content:
        with st.expander("Document Preview", expanded=True):
            st.markdown(st.session_state.document_content)
    
    # Criteria input
    st.header("Processing Criteria")
    criteria = st.text_area(
        "Enter criteria (one per line)",
        key="criteria",
        value="\n".join(st.session_state.criteria_list) if st.session_state.criteria_list else "",
        placeholder="Enter each criterion on a new line\nExample:\nClear structure\nConcise content",
        height=150
    )
    st.session_state.criteria_list = [c.strip() for c in criteria.split("\n") if c.strip()]
    
    # Show criteria preview
    if st.session_state.criteria_list:
        with st.expander("Processing Criteria", expanded=True):
            for i, criterion in enumerate(st.session_state.criteria_list, 1):
                st.write(f"{i}. {criterion}")
    
    # Configuration
    st.header("Workflow Configuration")
    max_revisions = st.slider("Maximum Revisions", 1, 5, 3, key="max_revisions")
    require_approval = st.checkbox("Require Approval", value=True, key="require_approval")
    
    if st.button("Process Document", key="process_btn", use_container_width=True):
        if not st.session_state.document_content:
            st.error("Please provide document content by uploading a file or entering text")
            return
            
        if not st.session_state.criteria_list:
            st.error("Please provide at least one processing criterion")
            return
            
        st.info("Starting document processing workflow...")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Create workflow configuration
        config = WorkflowConfig(
            criteria=st.session_state.criteria_list,
            max_revisions=max_revisions,
            require_approval=require_approval
        )
        
        # Initialize workflow
        workflow = DocumentWorkflow(config, st.session_state.client)
        
        # Process document with progress bar and state management
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        with st.spinner("Processing document..."):
            if st.session_state.processing_state is None:
                st.session_state.processing_state = "processing"
                
            try:
                # Display processing steps
                status_placeholder.info("Step 1: Document Generation")
                result = asyncio.run(workflow.run({
                    "document": DocumentState(content=st.session_state.document_content),
                    "config": config
                }))
                
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
