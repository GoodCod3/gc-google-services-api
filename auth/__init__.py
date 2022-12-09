from google.oauth2 import service_account


class Auth:
    def __init__(self, credentials_content, scopes) -> None:
        self.credentials_content = credentials_content
        self.scopes = scopes
        
    def get_credentials(self):
        credentials = service_account.Credentials.from_service_account_info(
        self.credentials_content,
        scopes=self.scopes)

        creds = credentials.with_subject('alvaro@makingscience.com')
        
        return creds
    
        # service = build('admin', 'directory_v1', credentials=creds)