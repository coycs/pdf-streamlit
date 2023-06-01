import streamlit as st
import fitz
import os
import re


def download_pdf(data, name):
    st.download_button(
        label="Download PDF: {}".format(name),
        data=data,
        file_name='{}.pdf'.format(name),
        mime='application/pdf',
    )


def resolve_toc(txt):
    toc_list = []
    for line in txt.split('\n'):
        # skip the blank line
        if line == "":
            continue
        toc = []
        m = re.match(r'^(\d), \"(.+)\", (\d)$', line).groups()
        toc.append(int(m[0]))
        toc.append(m[1])
        toc.append(int(m[2]))
        toc_list.append(toc)
    return toc_list

# source code
st.markdown("Source Code: [https://github.com/coycs/pdf-streamlit/blob/main/pages/1_add%20catalog.py](https://github.com/coycs/pdf-streamlit/blob/main/pages/1_add%20catalog.py)")

# catalog example
st.text("Catalog example: ")
code_body = '''
1, "Title", 1
2, "Title 1.1", 2
3, "Title 1.1.1", 3
3, "Title 1.1.2", 4
2, "Title 1.1", 5
1, "Title 2", 6
1, "Title 3", 7
'''
st.code(code_body)
st.text('''Each line, such as the '1, "Title 3", 7'
'1' is the level
'Title' is the title
'7' is the page number''')
st.text("Catalog example effect: ")
st.image("./imgs/catalog.png")

# enter catalog
txt = st.text_area(label="Please enter catalog", value="")
# upload file
pdf = st.file_uploader(
    "Upload PDF file", type=['pdf'], accept_multiple_files=False)
# add catalog
if st.button("Add catalog"):
    if txt == "":
        st.warning("Please enter catalog first!")
    elif pdf is None:
        st.warning("Please upload  catalog first!")
    else:
        file_name_full = pdf.name
        file_name = os.path.splitext(pdf.name)[0]
        file_type = os.path.splitext(pdf.name)[1][1:]
        doc = fitz.open(stream=pdf.read(), filetype="pdf")
        doc.set_toc(resolve_toc(txt))
        download_pdf(doc.write(), file_name+"_catalog")
