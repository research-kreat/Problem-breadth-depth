import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

llm = ChatGroq(temperature=0, groq_api_key="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", model_name="mixtral-8x7b-32768")

def generate_abstract(domain, sub_domain, title):
    prompt = ChatPromptTemplate.from_template(f"""
    You are provided with a title, domain, and sub-domain. Use these details to create a concise abstract for the user's problem.

    Domain:
    ```{domain}```

    Sub-domain:
    ```{sub_domain}```

    Title:
    ```{title}```

    Your task is to generate a 30-word abstract that accurately summarizes the problem described by the title, ensuring relevance to the given domain and sub-domain.
    """)
    chain = (prompt | llm | StrOutputParser())
    return chain.invoke({"domain": domain, "sub_domain": sub_domain, "title": title})

def generate_description(domain, sub_domain, title, abstract):
    prompt = ChatPromptTemplate.from_template("""
    You are provided with a title, domain, sub-domain, and an abstract. Use these details to create a detailed description of the user's problem.

    Domain:
    ```{domain}```

    Sub-domain:
    ```{sub_domain}```

    Title:
    ```{title}```

    Abstract:
    ```{abstract}```

    Your task is to generate a comprehensive and detailed description of the problem described by the title and abstract. Ensure that the description elaborates on the key points mentioned in the abstract and is relevant to the given domain and sub-domain.
    """)
    chain = (prompt | llm | StrOutputParser())
    return chain.invoke({"domain": domain, "sub_domain": sub_domain, "title": title, "abstract": abstract})

def generate_breadth_and_depth(domain, sub_domain, title, abstract, description):
    prompt = ChatPromptTemplate.from_template(f"""
    You are provided with a title, domain, sub-domain, an abstract, and a detailed description of the problem. Use these details to generate the problem breadth and depth by answering the 5Ws and 1H.

    Domain:
    ```{domain}```

    Sub-domain:
    ```{sub_domain}```

    Title:
    ```{title}```

    Abstract:
    ```{abstract}```

    Description:
    ```{description}```

    Your task is to provide a detailed response to the following questions:
    **What:** Define the Problem Statement. This is the type of question we ask in order to narrow the problem and focus in on key issues.
    **When:** Clearly identifying the time related aspects of the problem. When does the conflict occur? Is the key question here.
    **Where:** The 'Where?' key is relating to the ‘zones of conflict’. Determine what is the zone of conflict looking at the super-system, system and sub-system.
    **Who:** Clearly identify the person connected with the problem. He could be one who is using the final product or anyone in the line-up of concept-to-market or a person at any of the product Life-stages.
    **How:** The how question is present to encourage you to think about the underlying causes and effects of the problem. How does the conflict arise?

    Now think about these inverse questions:
    **What is not a Problem?**: In contrast to the above context of "what is the problem", identify what is not a problem in the current scenario.
    **When is it not a Problem?**: When is it not a problem or when is the time the conflict doesn't occur?
    **Where is it not a Problem?**: Identify the zones of conflict where the problem doesn't occur looking at the super-system, system, and sub-system.
    **Who is not affected?**: Here, identify the people who are not connected with the problem. They could be ones who are not using the final product or anyone not affected by the problem.
    **How is it not a Problem?**: The how-not question is present to encourage us to think about how it is not affecting the current environment.

    Provide comprehensive and relevant answers based on the given domain, sub-domain, title, abstract, and description.
    """)
    chain = (prompt | llm | StrOutputParser())
    return chain.invoke({"domain": domain, "sub_domain": sub_domain, "title": title, "abstract": abstract, "description": description})

# Initialize session state variables
if "domain" not in st.session_state:
    st.session_state.domain = ""
if "sub_domain" not in st.session_state:
    st.session_state.sub_domain = ""
if "title" not in st.session_state:
    st.session_state.title = ""
if "abstract" not in st.session_state:
    st.session_state.abstract = ""
if "description" not in st.session_state:
    st.session_state.description = ""
if "breadth_and_depth" not in st.session_state:
    st.session_state.breadth_and_depth = ""

def main():
    st.title("Problem Solver App")
    st.sidebar.header("Input")

    # Input fields
    st.session_state.domain = st.sidebar.text_input("Domain", value=st.session_state.domain)
    st.session_state.sub_domain = st.sidebar.text_input("Sub-domain", value=st.session_state.sub_domain)
    st.session_state.title = st.sidebar.text_input("Title", value=st.session_state.title)

    # Generate Abstract
    if st.sidebar.button('Generate Abstract'):
        st.session_state.abstract = generate_abstract(st.session_state.domain, st.session_state.sub_domain, st.session_state.title)
    
    # Display Abstract
    if st.session_state.abstract:
        st.header("Abstract")
        st.write(st.session_state.abstract)

    # Generate Description
    if st.sidebar.button('Generate Description'):
        st.session_state.description = generate_description(st.session_state.domain, st.session_state.sub_domain, st.session_state.title, st.session_state.abstract)
    
    # Display Description
    if st.session_state.description:
        st.header("Description")
        st.write(st.session_state.description)

    # Generate Breadth and Depth
    if st.sidebar.button('Generate Breadth and Depth'):
        st.session_state.breadth_and_depth = generate_breadth_and_depth(st.session_state.domain, st.session_state.sub_domain, st.session_state.title, st.session_state.abstract, st.session_state.description)
    
    # Display Breadth and Depth
    if st.session_state.breadth_and_depth:
        st.header("Problem Breadth and Depth")
        st.write(st.session_state.breadth_and_depth)

if __name__ == "__main__":
    main()
