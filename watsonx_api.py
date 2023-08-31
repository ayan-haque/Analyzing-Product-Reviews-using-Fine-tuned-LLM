from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models import Model

import os
import json
import prompt_generation

my_credentials = {
    "url"    : "https://us-south.ml.cloud.ibm.com",
    "apikey" : os.environ.get('WATSONX_API_KEY')
}   


model_id    = ModelTypes.FLAN_UL2
#gen_parms   = {GenParams.MAX_NEW_TOKENS: 200, GenParams.TOP_P: 0.3, GenParams.TOP_K: 3}
gen_parms   = {GenParams.MAX_NEW_TOKENS: 200, GenParams.TOP_P: 0.3, GenParams.TOP_K: 3, GenParams.REPETITION_PENALTY:1.3,
               GenParams.DECODING_METHOD: 'greedy', GenParams.TEMPERATURE: 0.2, GenParams.RANDOM_SEED: 33}
project_id  = os.environ.get('PROJECT_ID')
space_id    = None
verify      = False
model = Model( model_id, my_credentials, gen_parms, project_id, space_id, verify)   
gen_parms_override = None


# Defining separate 'gen_parms' for extracting sentiment related keywords
gen_parms_sentiment_keywords   = {GenParams.MAX_NEW_TOKENS: 200, GenParams.TOP_P: 0.3, GenParams.TOP_K: 3,
               GenParams.DECODING_METHOD: 'greedy', GenParams.TEMPERATURE: 0.2, GenParams.RANDOM_SEED: 33}



# Defining the Model with corresponding  'gen_parms_sentiment_keywords'
model_sentiment_keywords = Model( model_id, my_credentials, gen_parms_sentiment_keywords, project_id, space_id, verify)   


class checkReview:
    
    def __init__(self):
        pass
    
    def checkWatsonService(self):
        # Getting model details, to test whether watsonx.ai service is running fine
        model_details = model.get_details()
        model_details = json.dumps( model_details, indent=2 )
        return model_details
    
    def getEntities(self, input_review):
        
        '''
        Parameters
        ----------
        input_review : str
            This is input review from the user.

        Returns
        -------
        generated_response_entity_text : str
            Extracted entities from the review: PERSON, EMAIL, PHONE, PRODUCT, COMPETITOR

        '''
        
        input_entity_prompt = prompt_generation.generate_entity_prompt(input_review)
        print("\n \n")
        print("input_entity_prompt is: ", input_entity_prompt)
        print("\n \n")
        
        generated_response_entity = model.generate(input_entity_prompt, gen_parms_override)
        generated_response_entity_text  = json.dumps( generated_response_entity['results'][0]['generated_text'], indent=2 )
        
        print("\n \n")
        print("Generated_response_text for entity extraction is: ", generated_response_entity_text)
        
        #return input_entity_prompt
        return generated_response_entity_text
    
    
    
    def getSentiment(self, input_review):
        
        '''
        Parameters
        ----------
        input_review : str
            This is input review from the user.

        Returns
        -------
        generated_response_sentiment_text : str
            Sentiment the review: Positive, Negative, Neutral

        '''
        
        input_sentiment_prompt = prompt_generation.generate_sentiment_prompt(input_review)
        print("\n \n")
        print("input_sentiment_prompt is: ", input_sentiment_prompt)
        print("\n \n")
        
        #generated_response_sentiment = model.generate(input_sentiment_prompt, gen_parms_override)
        generated_response_sentiment = model_sentiment_keywords.generate(input_sentiment_prompt, gen_parms_override)
        generated_response_sentiment_text  = json.dumps( generated_response_sentiment['results'][0]['generated_text'], indent=2 )
        
        print("\n \n")
        print("Generated_sentiment_text for sentiment classification: ", generated_response_sentiment_text)
        
        return generated_response_sentiment_text
    
    
    def getSentimentContributingTexts(self, input_review, sentiment):
        
        # Now based on the 'sentiment' (positive / negative / mixed), we will generate corresponding input prompt
        # 1) Generating prompt if sentiment is positive
        if ("positive" in sentiment) or ("negative" in sentiment): 

            # str prompt for extracting postive or negative contributing keywords
            input_sentiment_keywords_prompt = prompt_generation.generate_sentiment_keywords_prompt(input_review, sentiment)
            print("\n HERE... input_sentiment_keywords_prompt is: ", input_sentiment_keywords_prompt)
            print("\n")
            
            # Calling model
            generated_response_response_sentiment_ContibTexts = model_sentiment_keywords.generate( input_sentiment_keywords_prompt, gen_parms_override )  # dict
            generated_response_response_sentiment_ContibTexts  = json.dumps( generated_response_response_sentiment_ContibTexts['results'][0]['generated_text'], indent=2 )  # str
            
            return generated_response_response_sentiment_ContibTexts
        
        
        
        elif ("mixed" in sentiment): 
            sentiment = "Mixed"
            
            # dict for extracting positve and negative contributing keywords separately
            input_sentiment_keywords_prompt = prompt_generation.generate_sentiment_keywords_prompt(input_review, sentiment)
            print("\n input_sentiment_keywords_prompt (watson_api.py) : ", input_sentiment_keywords_prompt)
            
            # 1) Extracting positve contributing keywords
            input_sentiment_keywords_prompt_POSITIVE = input_sentiment_keywords_prompt["sentiment_keywords_prompt_mixed_POSITIVE"]
            
            # 2) Extracting negative contributing keywords
            input_sentiment_keywords_prompt_NEGATIVE = input_sentiment_keywords_prompt["sentiment_keywords_prompt_mixed_NEGATIVE"]
            
            # 1a) # Calling model for Positive sentiment texts
            generated_response_response_sentiment_ContibTexts_POSITIVE = model_sentiment_keywords.generate( input_sentiment_keywords_prompt_POSITIVE, gen_parms_override )  # dict
            generated_response_response_sentiment_ContibTexts_POSITIVE  = json.dumps( generated_response_response_sentiment_ContibTexts_POSITIVE['results'][0]['generated_text'], indent=2 )  # str
            
            
            # 2a) # Calling model for Negative sentiment texts
            generated_response_response_sentiment_ContibTexts_NEGATIVE = model_sentiment_keywords.generate( input_sentiment_keywords_prompt_NEGATIVE, gen_parms_override )  # dict
            generated_response_response_sentiment_ContibTexts_NEGATIVE  = json.dumps( generated_response_response_sentiment_ContibTexts_NEGATIVE['results'][0]['generated_text'], indent=2 )  # str
            
            
            return {"generated_response_response_sentiment_ContibTexts_POSITIVE": generated_response_response_sentiment_ContibTexts_POSITIVE,
                    "generated_response_response_sentiment_ContibTexts_NEGATIVE": generated_response_response_sentiment_ContibTexts_NEGATIVE}
    
    def getSummary(self, input_review):
        
        '''
        Parameters
        ----------
        input_review : str
            This is input review from the user.

        Returns
        -------
        generated_response_summary_text : str
            Short summary of the review

        '''
        
        # Modifying 'GenParams' to get dynamic summary
        gen_parms_summary   = {GenParams.MAX_NEW_TOKENS: 200, GenParams.TOP_P: 0.5, GenParams.TOP_K: 50, GenParams.REPETITION_PENALTY:1.3,
                       GenParams.DECODING_METHOD: 'sample', GenParams.TEMPERATURE: 1.8}
        model_s = Model( model_id, my_credentials, gen_parms_summary, project_id, space_id, verify)   
        
        input_summary_prompt = prompt_generation.generate_summary_prompt(input_review)
        print("\n \n")
        print("input_summary_prompt is: ", input_summary_prompt)
        print("\n \n")
        
        generated_response_summary = model_s.generate(input_summary_prompt, gen_parms_override)
        generated_response_summary_text  = json.dumps( generated_response_summary['results'][0]['generated_text'], indent=2 )
        
        
        print("\n \n")
        print("Generated_response_summary_text for Summary is: ", generated_response_summary_text)
        
        return generated_response_summary_text
    
    
    
        
        