import json
    
def generate_entity_prompt(input_review):

    '''
    Parameters
    ----------
    input_review : str
        This is input review from the user.

    Returns
    -------
    entity_prompt : str
        prompt to be used as input to LLM for entity extraction.

    '''
    # Loading example entity data from the file
    with open('examples/examples_NER.json', 'r') as file:
        examples_data_NER = json.load(file)
    
    examples_data_NER_str = ""
    for item in examples_data_NER:
        i_examples_data_NER_str = str(item) + "\n"
        examples_data_NER_str = examples_data_NER_str + i_examples_data_NER_str + "\n"

    entity_prompt = f"""Given a product review as input. You have to extract the following entities from it, (only if they are present): 1) Person, 2) Email, 3) Phone, 4) Product, 5) Competitor. \n
    You can consider the following examples of reviews and corresponing extracted entities to see how it should be done. Here are examples: \n <start of examples> \n {examples_data_NER_str} \n <end of examples> \n
    Now, here's the review enclosed within 3 backticks from which you have to extract entities: \n <start of review> ``` {input_review} ``` <end of review> 
    Most Important point to note: a) Aways keep the structure of your 'Entities' response as illutrated in examples i.e. {{'Person':[<extracted entities if any, else NULL>], 'Email':[<extracted entities if any, else NULL>], 'Phone':[<extracted entities if any, else NULL>], 'Product': [<extracted entities if any, else NULL>], 'Competitor':[<extracted entities if any, else NULL>]}} . b) In your response, only give extracted entities from the review and not from any examples. c) If entities are not present return 'NULL', do not hallucinate, cross check your response and do not provide fake entities.
    """

    return entity_prompt




def generate_sentiment_prompt(input_review):
    
    '''
    Parameters
    ----------
    input_review : str
        This is input review from the user.

    Returns
    -------
    sentiment_prompt : str
        prompt to be used as input to LLM for sentiment classification.

    '''
    
    #sentiment_prompt = f"""Provide the sentiment (Positive / Negative / Neutral) of this product review: ```{input_review}``` """
    sentiment_prompt =  f"""Provide the sentiment (Positive / Negative / Mixed / Neutral) of this product review: <start of review>```{input_review}```<end of review>. NOTE: If you find both positive and negative instances then give 'Mixed' as output"""
    
    return sentiment_prompt




def generate_sentiment_keywords_prompt(input_review, sentiment):
    
    i_sentiment =""
    
    # sentiment = positive / negative / mixed
    if ("positive" in sentiment):
        i_sentiment = "Positive"
        print("sentiment: ", sentiment)
        print("i_sentiment: ", i_sentiment)
        #sentiment_keywords_prompt = f"""Here's the product review enclosed within 3 backsticks: <start of review>```{input_review}```<end of review>. \n Now tell me which parts of the the review contibuted most in deciding the sentiment as {i_sentiment} ?. IMPORTANT NOTE: a) If more than one part contribute for the review being {i_sentiment}, then list all those parts"""
        sentiment_keywords_prompt = f"""Here's the product review enclosed within 3 backsticks: <start of review>```{input_review}```<end of review>. \n Now give out all those parts of the the review which contibuted in deciding the sentiment as {i_sentiment}. IMPORTANT NOTE: a) If more than one part contribute for the review being {i_sentiment}, then give all those parts"""
        
        return sentiment_keywords_prompt  # str is returned with single prompt
    
    
    elif ("negative" in sentiment):
        i_sentiment = "Negative"
        #sentiment_keywords_prompt = f"""Here's the product review enclosed within 3 backsticks: <start of review>```{input_review}```<end of review>. \n Now tell me which parts of the the review contibuted most in deciding the sentiment as {i_sentiment} ?. IMPORTANT NOTE: a) If more than one part contribute for the review being {i_sentiment}, then list all those parts"""
        sentiment_keywords_prompt = f"""Here's the product review enclosed within 3 backsticks: <start of review>```{input_review}```<end of review>. \n Now give out all those parts of the the review which contibuted in deciding the sentiment as {i_sentiment}. IMPORTANT NOTE: a) If more than one part contribute for the review being {i_sentiment}, then give all those parts"""
        
        return sentiment_keywords_prompt  # str is returned with single prompt
    
    
    
    elif sentiment == "Mixed":
        sentiment_positive = "Positive"
        sentiment_keywords_prompt_mixed_POSITIVE = f"""Here's the product review enclosed within 3 backsticks: <start of review>```{input_review}```<end of review>. \n Now tell me which parts of the the review contibuted most in deciding the sentiment as {sentiment_positive}?. IMPORTANT NOTE: a) If more than one part contribute for the review being {sentiment_positive}, then list all those parts"""
        
        sentiment_negative = "Negative"
        sentiment_keywords_prompt_mixed_NEGATIVE = f"""Here's the product review enclosed within 3 backsticks: <start of review>```{input_review}```<end of review>. \n Now tell me which parts of the the review contibuted most in deciding the sentiment as {sentiment_negative}?. IMPORTANT NOTE: a) If more than one part contribute for the review being {sentiment_negative}, then list all those parts"""
        
        print("\n INSIDE MIXED Sentiment")
        print("sentiment_positive: ", sentiment_positive)
        print("sentiment_negative: ", sentiment_negative)
        
        # dict is returned with two prompts for generative positive and negative texts separately
        return {"sentiment_keywords_prompt_mixed_POSITIVE": sentiment_keywords_prompt_mixed_POSITIVE,
                "sentiment_keywords_prompt_mixed_NEGATIVE": sentiment_keywords_prompt_mixed_NEGATIVE}
    

def generate_summary_prompt(input_review):

    '''
    Parameters
    ----------
    input_review : str
        This is input review from the user.

    Returns
    -------
    summary_prompt : str
        prompt to be used as input to LLM to generate summary.

    '''
    
    # Loading example summary data from the file
    with open('examples/examples_summary.json', 'r') as file:
        examples_data_summary = json.load(file)

    examples_data_summary_str = ""
    for item in examples_data_summary:
        i_examples_data_summary_str = str(item) + "\n"
        examples_data_summary_str = examples_data_summary_str + i_examples_data_summary_str + "\n"
        
        
    summary_prompt = f"""Given a product review as input. You have to generate a shorter summary of that review.
    You can consider the following examples of reviews and their corresponing summary to see how it should be done. Here are examples: \n <start of examples> \n {examples_data_summary_str} \n <end of examples> \n 
    Now, here's the review enclosed within 3 backticks from which you have to generate a short summary: \n <start of review> ``` {input_review} ``` <end of review>  
    Important point to note: a) Only provide generated summary in your response. b) Most important, do not exceed the generated summary length by 250 characters. c) Do not repeat review in your response.
    """
    
    return summary_prompt





     
     