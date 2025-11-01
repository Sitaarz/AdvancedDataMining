import os

class AppSettings:
    api_key = None
    start_from_id = None
    stop_at_id = None

    @staticmethod
    def load_settings(path: str):
        import json
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            AppSettings.api_key = data['apiKey'] if os.getenv('API_KEY') is None else os.getenv('API_KEY')
            AppSettings.start_from_id = data.get('startFromId') if os.getenv('START_FROM_ID') is None else os.getenv('START_FROM_ID')
            AppSettings.stop_at_id = data.get('stopAtId') if os.getenv('STOP_AT_ID') is None else os.getenv('STOP_AT_ID')
