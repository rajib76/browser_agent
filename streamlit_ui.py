import streamlit as st

from llms.openai_client import BrowseWeb
from selenium_ops.browse_a_site_scroll import BrowseASite


def get_links(query):
    # Placeholder function to simulate fetching links
    bweb = BrowseWeb()
    response = bweb.generate_web_link(query)
    print(response)
    basite = BrowseASite(url=response)
    # prompt = "Extract only the hyperlink of the arxiv papers in the image"
    final_list_url = basite.browse_site()

    print("final ", final_list_url)
    return final_list_url


def generate_summary(link):
    # Placeholder function to simulate generating a summary for the selected link
    bweb = BrowseWeb()
    pdf_filename = str(link).split("/abs/")[1]+"v1.pdf"
    reformatted_link = str(link).replace("abs","pdf")
    print("reformatted ",reformatted_link)
    basite = BrowseASite(url=reformatted_link,type="SUMMARY")
    text = basite.summarize_pdf(pdf_filename)
    summary = bweb.summarize_content(text=text)

    return summary,reformatted_link


# Title for the app
st.title('Research Tool')

# Initialize session state for links if not already present
if 'links' not in st.session_state:
    st.session_state['links'] = []
if 'selected_link' not in st.session_state:
    st.session_state['selected_link'] = None

# Input field for the query
query = st.text_input('Ask your research question:')

# Button to submit the query
if st.button('Submit'):
    if query:
        st.session_state['links'] = get_links(query)  # Store links in session state
        st.session_state['selected_link'] = None  # Reset selected link
    else:
        st.error('Please enter a query.')

# Display a listbox with the links
if st.session_state['links']:
    st.session_state['selected_link'] = st.selectbox('Select a link to summarize:', st.session_state['links'])

# Button to generate summary
if st.button('Generate Summary'):
    with st.spinner('Preparing the summary...'):
        if st.session_state['selected_link']:
            summary,reformatted_link = generate_summary(st.session_state['selected_link'])
            st.write('The summary will be presented here:')
            st.write(summary)
            st.markdown(reformatted_link)
        else:
            st.error('Please select a link first.')
