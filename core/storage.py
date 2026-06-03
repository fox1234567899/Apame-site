from supabase import create_client 
from django.core.files.storage import Storage 
from django.conf import settings 


class SupabaseStorage(Storage):
    def __init__(self):
        self.client=create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY

        )
        self.bucket = settings.SUPABASE_BUCKET_NAME
    

    def save(self,name,content):
        file_ext=name.split('.')[-1]
        file_name= f"{uuid.uuid4()}.{file_ext}"

        self.client.storage.from_(self.bucket).upload(
            file_name,
            content.read()
        )
        return file_name
    

    def url(self,name):
        return self.client.storage.from_(self.bucket).get_public_url(name)