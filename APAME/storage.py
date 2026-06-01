from django_supabase_storage import SupabaseMediaStorage


storage = SupabaseMediaStorage()
path = storage.save('media/img',content)
url=storage.url(path)