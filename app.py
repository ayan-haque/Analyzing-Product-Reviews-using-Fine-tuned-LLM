import streamlit as st
import helper_functions
import sys

st.markdown(
    """
    <style>
    .stButton>button {
        margin: 0 auto;
        display: block;
    }
    
    .output {
        background-color: #e0f0ff;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    
    .st-spinner {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    }
    


    """,
    unsafe_allow_html=True,
)




# Creating the Streamlit app page

# Adding link to my GitHub repository
github_link = """
<div style='float: right;'>
    <a href='https://github.com/amaan-ai/Product-Review-Analyzer-App-watsonxai'>
        <img src='https://img.shields.io/badge/GitHub-Repo-green?style=flat-square&logo=github'>
    </a>
</div>
"""
st.markdown(github_link, unsafe_allow_html=True)

# Adding a header and project description
st.title("Review Analyzer App - Watsonx.ai")
st.write("One-stop solution for Review Analysis: Entity detection (PERSON, EMAIL, PHONE, PRODUCT, COMPETITOR), Sentiment assessment, and concise summarization.")

# Creating a layout with two columns
#col1, col2 = st.columns(2)

# Creating the columns with a spacer column in between
col1, spacer, col2 = st.columns([3, 0.2, 4])  # Adjust the 0.1 value to increase or decrease the space


# In the left column, creating a text area for user input
with col1:
    st.write("Please enter a review below:")
    max_chars_length = 3000
    #input_text = st.text_area("", height=300, max_chars=max_chars_length)  # Default height is set to 300 pixels, you can adjust as needed
    input_text = st.text_area("", placeholder="(min 60 chars)", height=300, max_chars=max_chars_length)
    
# In the right column, displaying the output text (initially empty)
with col2:
    st.write("Output:")
    # We'll initialize this with an empty string, but it will be updated later
    output_text_area = st.empty()

# Creating a button below the columns
run = st.button("Check Review")
if run:
    
    # 0. Testing Watsonx.ai service
    try:
        from watsonx_api import checkReview
        checkReview_obj = checkReview()
        
        model_details = checkReview_obj.checkWatsonService()
        print("watsonx model running fine.. Here are model_details: ", model_details)
    except:
        st.write("If you're seeing this message, probably my free quota of watsonx service for this month has expired...")
        sys.exit()
        
    
    
    
    
    # Adding a check for minimum length of review
    if len(input_text) > 60 and input_text.isspace()==False:
        input_text = str(input_text)
        
    else:
        st.error("Review length too short to analyze. Please re-run with longer review. Thanks!")
        st.stop()
    
    # Adding a check for maximum length of review
    if len(input_text) > max_chars_length:
        st.error("Length of you Review exceeds 3000 characters. Please re-run with shorter review. Thanks!")
        st.stop()
    
    # 1. Extracting entities from review 
    with st.spinner('Checking presence of entities...'):
        # BELOW line only for testing 
        #input_text =  "I recently purchased the Galaxy S25 from Samsung, and I must say I'm thoroughly impressed. The battery life is phenomenal, and the camera quality is top-notch. However, I did face some issues with the customer support team when I tried reaching out to them at support@samsung.com. I also found that the iPhone 14 has a slightly better user interface." # TESTING
        entities = checkReview_obj.getEntities(input_text) # str
        
        try:  # Will try reformatting the entities
            entities_cleaned = helper_functions.transform_NER_output(entities)
            FLAG = "Success"
            
        except:  # Will try reformatting faulty entities
            try:
                entities_cleaned = helper_functions.transform_faulty_NER_output(entities)
                FLAG = "Success"
            except:
                FLAG = "Fail"
                
            
        if FLAG == "Fail":  # Otherwise return in old dict format
            entities_cleaned = entities
            
        # entities_cleaned = "Here are detected Entities: \n" + entities_cleaned

        
    # 2. Getting sentiment of the review 
    with st.spinner('Checking sentiment of the review...'):
        sentiment = checkReview_obj.getSentiment(input_text) # str
        # sentiment_text = "Sentiment: \n" + sentiment
        sentiment_text = sentiment
        
        
    # 3. Getting sentiment contributing texts in the review 
    sentiment = sentiment.lower()
    if ("positive" in sentiment) or ("negative" in sentiment):

        with st.spinner('Getting sentiment contributing texts...'):
            # str response  
            # # Getting Positive / Negative Sentiment texts
            sentiment_contributing_texts = checkReview_obj.getSentimentContributingTexts(input_text, sentiment) # str  # input_text = input_review
            
            sentiment_out = ""
            if ("positive" in sentiment):
                sentiment_out = "positively"
            elif ("negative" in sentiment):
                sentiment_out = "negatively"
                
            sentiment_contributing_texts = f"""For the above sentiment, these factors contributed {sentiment_out} :  \n""" + sentiment_contributing_texts
            
            
    elif ("mixed" in sentiment):
        with st.spinner('Getting mixed sentiment contributing texts...'):
            # dict response
            sentiment_contributing_texts_dict = checkReview_obj.getSentimentContributingTexts(input_text, sentiment) # str  # input_text = input_review
            
            
            # Getting Positive Sentiment texts
            sentiment_contributing_texts_POSITIVE = sentiment_contributing_texts_dict["generated_response_response_sentiment_ContibTexts_POSITIVE"]
            sentiment_contributing_texts_POSITIVE = "For the above sentiment, these factors contributed Positively:  \n" + sentiment_contributing_texts_POSITIVE
            
            # Getting Negative Sentiment texts
            sentiment_contributing_texts_NEGATIVE = sentiment_contributing_texts_dict["generated_response_response_sentiment_ContibTexts_NEGATIVE"]
            sentiment_contributing_texts_NEGATIVE = "For the above sentiment, these factors contributed Negatively:  \n" + sentiment_contributing_texts_NEGATIVE
            
            sentiment_contributing_texts = sentiment_contributing_texts_POSITIVE + "\n\n" +  sentiment_contributing_texts_NEGATIVE
            
    else:
        # Skipping sentiment contributing texts as sentiment is neutral
        sentiment_contributing_texts = ""
        pass
        
        
    # 4. Getting one line summary of the review
    with st.spinner('Getting one line summary of the review...'):
        summary = checkReview_obj.getSummary(input_text) # str
        #summary = "Summary: \n" + summary
        
    

     

    def custom_subheader(text, size=18):
        return st.markdown(f'<div style="font-size: {size}px; font-weight: bold">{text}</div>', unsafe_allow_html=True)
    
    # Custom horizontal line function with reduced spacing
    def custom_horizontal_line():
        st.markdown('<hr style="margin: 0.3rem 0;">', unsafe_allow_html=True)
    

    with col2:
        # 1. Displaying detected entities:
        custom_subheader("Detected Entities", size=16)
        
        # styling / Colouring entities
        if FLAG == "Success":
            entities_cleaned_styled = helper_functions.StyleColourEntities(entities_cleaned)
        else:
            entities_cleaned_styled = entities_cleaned
        #st.write(entities_cleaned)
        #st.write("---")  # This adds a horizontal line for separation
        st.markdown(entities_cleaned_styled, unsafe_allow_html=True)
        custom_horizontal_line()
    
        # 2. Displaying sentiment and contributing factors:
        custom_subheader("Sentiment Analysis", size=16)
        if "Mixed" in sentiment_text:
            st.write("Sentiment:", sentiment_text)
        else:
            st.write(sentiment_text)
        st.write(sentiment_contributing_texts)
        #st.write("---")  # This adds a horizontal line for separation
        custom_horizontal_line()
    
        # 3. Displaying the review summary:
        custom_subheader("Review Summary", size=16)
        st.write(summary)
        #st.write("---")  # This adds a horizontal line for separation
        custom_horizontal_line()






