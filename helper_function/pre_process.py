import spacy
from spacy.cli import download
import nltk
from main import app_logger, pd
import numpy as np
from transformers import pipeline

try:
    from nltk.corpus import stopwords
    app_logger.info(" Found Downloaded stopwords" )
except OSError:
    app_logger.info("Attempting to Download stopwords...")
    nltk.download('stopwords')
    from nltk.corpus import stopwords

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    app_logger.info("Attempting to Download 'en_core_web_sm' model...")
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")
    
doc = nlp("This is an example sentence.")
tokens = [token.text for token in doc]
app_logger.info(f"Example of tokenization: '{doc}'  >> \n {tokens}")


def text_tokenization(text:str) ->str :

    nltk_stopwords = set(stopwords.words('english'))
    medical_stopwords = set(['drug', 'treatment', 'tablet', 'dose'])
    text = str(text)  # Convert input to string
    doc = nlp(text)
    tokens = [
        token.lemma_.lower()
        for token in doc
        if (token.is_alpha or token.is_digit) and token.lemma_.lower() not in nltk_stopwords | medical_stopwords
    ]

    app_logger.debug(f"Text Tokenization >>> Removing stops words....")

    return " ".join(tokens)




def sentiment_polarities(df, rating:str, limit:list=[8,3] )-> pd.DataFrame:

    conditions = [
        df[rating] >= max(limit),
        df[rating] <= min(limit)
    ]
    choices = ['positive', 'negative']

    df.loc[:, 'sentiment_rating']  = np.select(conditions, choices, default='neutral')
    
    app_logger.info(f"Polarities assigned for the system generated column")

    return df

def text_cleaning(drug_train_raw, cols_to_concat:list=None,
                  )->pd.DataFrame :

    app_logger.info(f"text cleaning processing for assigned dataframe started...")

    # drug_train_raw["combined_text"] = drug_train_raw[cols_to_concat].sum(axis=1)

    drug_train_raw.loc[:, 'combined_text'] = (drug_train_raw[cols_to_concat].fillna('').astype(str).agg(' '.join, axis=1))
    # drug_train_raw['combined_text'] = drug_train_raw['benefitsReview'] + drug_train_raw['sideEffectsReview'] + drug_train_raw['commentsReview']
    drug_train_raw.loc[:,'combined_text'] = drug_train_raw['combined_text'].fillna('')
    drug_train_raw.loc[:,'clean_text'] = drug_train_raw['combined_text'].apply(text_tokenization)

    app_logger.info(f"Removing stopwords process completed>>> scanned {sum(drug_train_raw['combined_text'].str.split().str.len())} words")

    return drug_train_raw

def text_transformer(df:pd.DataFrame, cleaned_texts_col_name:str,
                     mdl_name:str ="distilbert-base-uncased-finetuned-sst-2-english" 
                     )-> pd.DataFrame:
    # Load a pre-trained sentiment analysis model
    # 'distilbert-base-uncased-finetuned-sst-2-english' >> lightweight option
    sentiment_classifier = pipeline(
        "sentiment-analysis",
        model=str(mdl_name)
    )
    app_logger.info(f"processing {len(df)} records for sentiment {cleaned_texts_col_name} analysis")
    predictions = sentiment_classifier(df[cleaned_texts_col_name].tolist())

    df['mdl_sentiment_lbl'] = [lbl["label"] for lbl in predictions]
    df['mdl_lbl_score'] = [score['score'] for score in predictions]

    return df

def generate_text_transformation(df:pd.DataFrame,cols_to_concat:list, 
                                polarities_limit:list=[8,3], sys_col_rating_nm:str="rating", 
                                mdl_name:str ="distilbert-base-uncased-finetuned-sst-2-english")-> pd.DataFrame:
    

    df = sentiment_polarities(df,sys_col_rating_nm, polarities_limit )
    
    clean_txt_df = text_cleaning(df, cols_to_concat)
    clean_txt_df.drop('combined_text', axis=1, inplace=True)

    clean_txt_df.to_csv('../data/raw/drug_train_clean_text.csv', index=False)
    app_logger.info(f"processed clean text df..saving at intermediate location >>> data/raw/ ")

    transformed_df = text_transformer(clean_txt_df,'clean_text', mdl_name)
    transformed_df = transformed_df.copy()
    transformed_df.drop(cols_to_concat+['clean_text'], axis=1, inplace=True)

    app_logger.info(f"Transformation completed >>>> saving file data/processed")
    transformed_df.to_csv('../data/processed/drug_transformed.csv', index=False)

    return transformed_df








