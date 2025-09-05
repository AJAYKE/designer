import aioboto3
import json
from typing import Optional, Dict, Any
from app.core.config import settings
from app.models.design_state import GeneratedScreen
import aiofiles
from datetime import datetime

class S3Service:
    def __init__(self):
        self.bucket_name = settings.S3_BUCKET_NAME
        self.region = settings.AWS_REGION
        
    async def store_generated_screen(
        self, 
        thread_id: str, 
        message_id: str, 
        screen: GeneratedScreen
    ) -> str:
        """
        Store a generated screen in S3 with organized structure:
        /designs/{thread_id}/{message_id}/{screen_id}/
        """
        
        try:
            session = aioboto3.Session()
            
            async with session.client(
                's3',
                region_name=self.region,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            ) as s3:
                
                # Create organized folder structure
                base_path = f"designs/{thread_id}/{message_id}/{screen.screen_id}"
                
                # Store HTML file
                html_key = f"{base_path}/index.html"
                await s3.put_object(
                    Bucket=self.bucket_name,
                    Key=html_key,
                    Body=screen.html_code,
                    ContentType='text/html',
                    Metadata={
                        'screen-type': screen.metadata.screen_type.value,
                        'thread-id': thread_id,
                        'message-id': message_id,
                        'generated-at': datetime.utcnow().isoformat()
                    }
                )
                
                # Store CSS file (if exists)
                if screen.css_classes:
                    css_key = f"{base_path}/styles.css"
                    await s3.put_object(
                        Bucket=self.bucket_name,
                        Key=css_key,
                        Body=screen.css_classes,
                        ContentType='text/css'
                    )
                
                # Store JavaScript file (if exists)
                if screen.javascript:
                    js_key = f"{base_path}/script.js"
                    await s3.put_object(
                        Bucket=self.bucket_name,
                        Key=js_key,
                        Body=screen.javascript,
                        ContentType='application/javascript'
                    )
                
                # Store metadata as JSON
                metadata_key = f"{base_path}/metadata.json"
                metadata_json = json.dumps({
                    "screen_id": screen.screen_id,
                    "screen_type": screen.metadata.screen_type.value,
                    "title": screen.metadata.title,
                    "description": screen.metadata.description,
                    "generation_time_ms": screen.generation_time_ms,
                    "token_usage": screen.token_usage,
                    "images": screen.images,
                    "generated_at": datetime.utcnow().isoformat()
                }, indent=2)
                
                await s3.put_object(
                    Bucket=self.bucket_name,
                    Key=metadata_key,
                    Body=metadata_json,
                    ContentType='application/json'
                )
                
                # Return the base S3 URL for the screen
                return f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{base_path}/"
        
        except Exception as e:
            print(f"❌ S3 Storage Error: {e}")
            raise
    
    async def store_user_edit(
        self,
        thread_id: str,
        message_id: str,
        screen_id: str,
        edited_html: str,
        user_id: str
    ) -> str:
        """Store user-edited version of a screen"""
        
        try:
            session = aioboto3.Session()
            
            async with session.client(
                's3',
                region_name=self.region,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            ) as s3:
                
                # Store in edits subfolder
                edit_key = f"designs/{thread_id}/{message_id}/{screen_id}/edits/{user_id}_{datetime.utcnow().isoformat()}.html"
                
                await s3.put_object(
                    Bucket=self.bucket_name,
                    Key=edit_key,
                    Body=edited_html,
                    ContentType='text/html',
                    Metadata={
                        'edited-by': user_id,
                        'original-screen-id': screen_id,
                        'edit-timestamp': datetime.utcnow().isoformat()
                    }
                )
                
                return f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{edit_key}"
                
        except Exception as e:
            print(f"❌ S3 Edit Storage Error: {e}")
            return None
    
    async def get_screen_content(self, thread_id: str, message_id: str, screen_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve screen content from S3"""
        
        try:
            session = aioboto3.Session()
            
            async with session.client(
                's3',
                region_name=self.region,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            ) as s3:
                
                base_path = f"designs/{thread_id}/{message_id}/{screen_id}"
                
                # Get HTML
                html_response = await s3.get_object(Bucket=self.bucket_name, Key=f"{base_path}/index.html")
                html_content = await html_response['Body'].read()
                
                # Get metadata
                metadata_response = await s3.get_object(Bucket=self.bucket_name, Key=f"{base_path}/metadata.json")
                metadata_content = await metadata_response['Body'].read()
                metadata = json.loads(metadata_content.decode('utf-8'))
                
                # Try to get CSS and JS (optional)
                css_content = ""
                js_content = ""
                
                try:
                    css_response = await s3.get_object(Bucket=self.bucket_name, Key=f"{base_path}/styles.css")
                    css_content = (await css_response['Body'].read()).decode('utf-8')
                except:
                    pass
                
                try:
                    js_response = await s3.get_object(Bucket=self.bucket_name, Key=f"{base_path}/script.js")
                    js_content = (await js_response['Body'].read()).decode('utf-8')
                except:
                    pass
                
                return {
                    "html": html_content.decode('utf-8'),
                    "css": css_content,
                    "javascript": js_content,
                    "metadata": metadata
                }
                
        except Exception as e:
            print(f"❌ S3 Retrieval Error: {e}")
            return None

