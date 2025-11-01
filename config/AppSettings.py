class AppSettings:
    api_key = None
    start_from_id = None
    stop_at_id = None

    @staticmethod
    def load_settings(path: str):
        import json
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            AppSettings.api_key = data['apiKey']
            AppSettings.start_from_id = data.get('startFromId')
            AppSettings.stop_at_id = data.get('stopAtId')
