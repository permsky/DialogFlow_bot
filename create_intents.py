import json
import os

from dotenv import load_dotenv
from google.cloud import dialogflow


def create_intent(
    project_id: str,
    display_name: str,
    training_phrases_parts: list,
    message_texts: str
) -> None:
    '''Create an intent of the given intent type.'''
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part
        )
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)
    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)
    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )
    intents_client.create_intent(
        request={'parent': parent, 'intent': intent}
    )


def main() -> None:
    '''Create new DialogFlow intents.'''
    load_dotenv()
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID')
    filepath = os.getenv('TRAINING_PHRASES_FILEPATH')
    with open(filepath, 'r', encoding='utf-8') as intents_file:
        intents = json.load(intents_file)

    for intent, intent_content in intents.items():
        create_intent(
            project_id=project_id,
            display_name=intent,
            training_phrases_parts=intent_content['questions'],
            message_texts=intent_content['answer']
        )


if __name__ == '__main__':
    main()
