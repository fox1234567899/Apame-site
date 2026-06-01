from django_supabase_storage import SupabaseMediaStorage
from django.core.files.storage import default_storage



storage = SupabaseMediaStorage()
path = storage.save('img/',content)
url=storage.url(path)