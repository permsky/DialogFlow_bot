from google.cloud import dialogflow
from google.cloud.dialogflow_v2.types.session import DetectIntentResponse


def detect_intent_text(
    project_id: str,
    session_id: str,
    text: str,
    language_code: str
) -> DetectIntentResponse:
    '''Returns the result of detect intent'''
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    return session_client.detect_intent(
        request={'session': session, 'query_input': query_input}
    )
