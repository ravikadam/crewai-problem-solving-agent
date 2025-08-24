import os
import json
from typing import Optional, Dict, Any
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class GoogleDocsInput(BaseModel):
    """Input schema for Google Docs creation."""
    title: str = Field(..., description="The title of the Google Doc")
    content: str = Field(..., description="The content to write to the document (markdown format)")


class GoogleDocsCreatorTool(BaseTool):
    name: str = "Google Docs Creator"
    description: str = (
        "Creates a new Google Doc with the specified title and content. "
        "Requires Google service account credentials or OAuth credentials."
    )
    args_schema: type[BaseModel] = GoogleDocsInput

    def _run(self, title: str, content: str) -> str:
        """Create a Google Doc with the given title and content."""
        try:
            # Try to get service account credentials
            service_account_path = os.getenv('GOOGLE_SERVICE_ACCOUNT_PATH')
            print(f'DEBUG: Using service account path: {service_account_path}')
            
            if service_account_path and service_account_path != "path/to/your/service-account.json" and os.path.exists(service_account_path):
                # Use service account
                print(f'DEBUG: Loading credentials from: {service_account_path}')
                print(f'DEBUG: File exists: {os.path.exists(service_account_path)}')
                
                # Read and verify the key content
                with open(service_account_path, 'r') as f:
                    import json
                    key_data = json.load(f)
                    print(f'DEBUG: Key ID: {key_data.get("private_key_id")}')
                    print(f'DEBUG: Client email: {key_data.get("client_email")}')
                
                credentials = service_account.Credentials.from_service_account_file(
                    service_account_path,
                    scopes=['https://www.googleapis.com/auth/drive.file', 
                           'https://www.googleapis.com/auth/documents']
                )
                print('DEBUG: Credentials loaded successfully')
            else:
                # Check for OAuth credentials in environment
                client_id = os.getenv('GOOGLE_CLIENT_ID')
                client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
                refresh_token = os.getenv('GOOGLE_REFRESH_TOKEN')
                
                if not all([client_id, client_secret, refresh_token]):
                    return (
                        "Google Docs API credentials not found. Please set up either:\n"
                        "1. Service Account: Set GOOGLE_SERVICE_ACCOUNT_PATH to your service account JSON file\n"
                        "2. OAuth: Set GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, and GOOGLE_REFRESH_TOKEN\n"
                        "See GOOGLE_SETUP.md for detailed instructions."
                    )
                
                credentials = Credentials(
                    token=None,
                    refresh_token=refresh_token,
                    token_uri="https://oauth2.googleapis.com/token",
                    client_id=client_id,
                    client_secret=client_secret
                )

            # Build the services
            docs_service = build('docs', 'v1', credentials=credentials)
            drive_service = build('drive', 'v3', credentials=credentials)
            
            # Create a new document
            doc = docs_service.documents().create(body={'title': title}).execute()
            doc_id = doc.get('documentId')
            
            # Convert markdown content to Google Docs format
            formatted_content = self._markdown_to_docs_format(content)
            
            # Insert content into the document
            requests = []
            for item in formatted_content:
                requests.append({
                    'insertText': {
                        'location': {'index': 1},
                        'text': item['text']
                    }
                })
                
                # Apply formatting if specified
                if 'format' in item:
                    requests.append({
                        'updateTextStyle': {
                            'range': {
                                'startIndex': 1,
                                'endIndex': 1 + len(item['text'])
                            },
                            'textStyle': item['format'],
                            'fields': ','.join(item['format'].keys())
                        }
                    })
            
            if requests:
                docs_service.documents().batchUpdate(
                    documentId=doc_id,
                    body={'requests': requests}
                ).execute()
            
            # Make the document publicly viewable (optional)
            try:
                drive_service.permissions().create(
                    fileId=doc_id,
                    body={
                        'role': 'reader',
                        'type': 'anyone'
                    }
                ).execute()
            except HttpError:
                # If permission setting fails, continue anyway
                pass
            
            doc_url = f"https://docs.google.com/document/d/{doc_id}/edit"
            
            return f"""
✅ Google Doc created successfully!

📄 Document Title: {title}
🔗 Document URL: {doc_url}
📋 Document ID: {doc_id}

The document has been created and is accessible via the URL above.
"""
            
        except HttpError as e:
            return f"Google API Error: {str(e)}"
        except Exception as e:
            return f"Error creating Google Doc: {str(e)}"
    
    def _markdown_to_docs_format(self, content: str) -> list:
        """Convert markdown content to Google Docs format."""
        lines = content.split('\n')
        formatted_content = []
        
        for line in lines:
            if line.startswith('# '):
                # Header 1
                formatted_content.append({
                    'text': line[2:] + '\n',
                    'format': {'bold': True, 'fontSize': {'magnitude': 20, 'unit': 'PT'}}
                })
            elif line.startswith('## '):
                # Header 2
                formatted_content.append({
                    'text': line[3:] + '\n',
                    'format': {'bold': True, 'fontSize': {'magnitude': 16, 'unit': 'PT'}}
                })
            elif line.startswith('### '):
                # Header 3
                formatted_content.append({
                    'text': line[4:] + '\n',
                    'format': {'bold': True, 'fontSize': {'magnitude': 14, 'unit': 'PT'}}
                })
            elif line.startswith('**') and line.endswith('**'):
                # Bold text
                formatted_content.append({
                    'text': line[2:-2] + '\n',
                    'format': {'bold': True}
                })
            elif line.startswith('- ') or line.startswith('* '):
                # Bullet points
                formatted_content.append({
                    'text': '• ' + line[2:] + '\n'
                })
            else:
                # Regular text
                formatted_content.append({
                    'text': line + '\n' if line.strip() else '\n'
                })
        
        return formatted_content


# Simplified version that creates plain text documents
class SimpleGoogleDocsCreatorTool(BaseTool):
    name: str = "Simple Google Docs Creator"
    description: str = (
        "Creates a simple Google Doc with plain text content. "
        "Requires Google service account credentials."
    )
    args_schema: type[BaseModel] = GoogleDocsInput

    def _run(self, title: str, content: str) -> str:
        """Create a simple Google Doc with plain text content."""
        try:
            service_account_path = os.getenv('GOOGLE_SERVICE_ACCOUNT_PATH')
            
            if not service_account_path or service_account_path == "path/to/your/service-account.json" or not os.path.exists(service_account_path):
                return (
                    "Google service account credentials not found. "
                    "Please set GOOGLE_SERVICE_ACCOUNT_PATH to your service account JSON file path."
                )
            
            credentials = service_account.Credentials.from_service_account_file(
                service_account_path,
                scopes=['https://www.googleapis.com/auth/documents', 
                       'https://www.googleapis.com/auth/drive']
            )
            
            docs_service = build('docs', 'v1', credentials=credentials)
            drive_service = build('drive', 'v3', credentials=credentials)
            
            # Create document
            doc = docs_service.documents().create(body={'title': title}).execute()
            doc_id = doc.get('documentId')
            
            # Insert content
            requests = [{
                'insertText': {
                    'location': {'index': 1},
                    'text': content
                }
            }]
            
            docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()
            
            # Make publicly viewable
            try:
                drive_service.permissions().create(
                    fileId=doc_id,
                    body={'role': 'reader', 'type': 'anyone'}
                ).execute()
            except:
                pass
            
            doc_url = f"https://docs.google.com/document/d/{doc_id}/edit"
            
            return f"✅ Google Doc created: {title}\n🔗 URL: {doc_url}\n📋 ID: {doc_id}"
            
        except Exception as e:
            return f"Error creating Google Doc: {str(e)}"
