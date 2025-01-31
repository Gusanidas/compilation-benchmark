import streamlit as st
import json
from typing import Dict, List, Optional

# Define input file path
INPUT_FILE = "results/2025-01-31.jsonl"

def load_jsonl(file_path: str) -> List[Dict]:
    """Load JSONL file and return list of dictionaries."""
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            data.append(json.loads(line.strip()))
    return data

def display_entry_card(entry: Dict) -> None:
    """Display main menu card for a single entry."""
    with st.container():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**ID:** {entry['id']}")
            st.write(f"**Model:** {entry['model']}")
            st.write(f"**Language:** {entry['programming_language']}")
        with col2:
            compilation_status = "✅" if entry['compilation_success'] else "❌"
            problem_correct = "✅" if entry['problem_correct'] else "❌"
            st.write(f"**Compilation:** {compilation_status}")
            st.write(f"**Problem Correct:** {problem_correct}")
            st.write(f"problem_id: {entry['problem_id']}")
        
        if st.button(f"View Details", key=f"btn_{entry['id']}"):
            st.session_state.selected_entry = entry
            st.session_state.view = "detail"

def display_detail_view(entry: Dict) -> None:
    """Display detailed view of a single entry."""
    st.write("# Entry Details")
    
    # Back button
    if st.button("← Back to Main Menu"):
        st.session_state.view = "main"
        st.session_state.selected_entry = None
        st.rerun()
    
    # Display all fields
    st.write("### Basic Information")
    st.write(f"**ID:** {entry['id']}")
    st.write(f"**Problem ID:** {entry['problem_id']}")
    st.write(f"**Model:** {entry['model']}")
    st.write(f"**Programming Language:** {entry['programming_language']}")
    
    st.write("### Status")
    st.write(f"**Compilation Success:** {'✅' if entry['compilation_success'] else '❌'}")
    st.write(f"**Runtime Success:** {'✅' if entry['runtime_success'] else '❌'}")
    
    st.write("### Code")
    st.code(entry['code'], language=entry['programming_language'].lower())
    
    if entry['code_errors']:
        st.write("### Errors")
        st.error(entry['code_errors'])

    if entry['output']:
        st.write("### Output")
        st.code(entry['output'], language="text")

def main():
    st.set_page_config(
        page_title="JSONL Viewer",
        page_icon="📄",
        layout="wide"
    )
    
    # Initialize session state
    if 'view' not in st.session_state:
        st.session_state.view = "main"
    if 'selected_entry' not in st.session_state:
        st.session_state.selected_entry = None
    
    try:
        # Load data from the specified file
        data = load_jsonl(INPUT_FILE)
        
        # Display appropriate view
        if st.session_state.view == "main":
            st.write("# JSONL Viewer")
            st.write(f"Total entries: {len(data)}")
            
            # Add search/filter options
            search_term = st.text_input("Search by ID or Model:", "")
            
            # Filter data based on search term
            if search_term:
                filtered_data = [
                    entry for entry in data 
                    if search_term.lower() in str(entry['id']).lower() 
                    or search_term.lower() in entry['model'].lower()
                ]
            else:
                filtered_data = data
            
            # Display entries
            for entry in filtered_data:
                st.divider()
                display_entry_card(entry)
                
        elif st.session_state.view == "detail" and st.session_state.selected_entry:
            display_detail_view(st.session_state.selected_entry)
    
    except FileNotFoundError:
        st.error(f"Error: Could not find the file '{INPUT_FILE}'")
        st.write("Please make sure the file exists in the correct location.")
    except json.JSONDecodeError:
        st.error(f"Error: Could not parse the JSONL file '{INPUT_FILE}'")
        st.write("Please make sure the file contains valid JSONL data.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()