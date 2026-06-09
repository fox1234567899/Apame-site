    I made the backend part of site with django


    In this part you can see how I made the user and how  manage the products 
    
    In products.models I made Item cartItem , cart, order, orderItem
    
    and transaction that you need it when you wanna pay the Items that you wanna buy

    so by making these things I kinda made a table just like in excel that we make

    that has rows and columns and based on information that customer would give us we 
    
    can fill the blanks.


    next we have the serializer that serializer is acting like the translator imagine 

    that we are in a trip so we hire a person who can talk with language of that people on that country

    why? maybe I could not understand the language of that person and that person either

    so translator know my language and know that person's language 

    in here serializer act as a translator react can't understand the django 

    nor the django. so at this part for their connection except of cors

    we need something to change their data to json so at this point they could change that json into 
    
    their own language 


    for example for detail part of the site we need the data such as id slug description 
    
    price, image, name  and similar_items 

    then in views.py we use these serializer and send it to react 

    like in itemview we called all the objects related to Item 

    and then we put them in the item serializer that we made in serializer

    just for giving these data to react and the react can use it in its own way.

    after that we put the views me made in urls.

    another thing is for my users I used the JWT that is for authentication access key and refresh

    but just becuase the jwt has its own technic for login i Kinda change it to something that I want it 

    for database  i was using the default database of django then change it 

    to postgres and then I use supabase . instead of using the local system

    I wanted my system save the data inside the supabase just to show and manage my data 

    easier 

    ## Add the supabase to your site 


    for connecting don't worry its not so hard if your site is working I mean the Upload or add delete or update

    then the only thing you want is :

    pip install django-supabase-storage    

    and then add this to settings:

    SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://your-project-id.supabase.co')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'your-anon-public-key')
    SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET_NAME", 'your-supabase-bucket-name')


    STORAGES = {
    'default': {
        'BACKEND': 'django_supabase_storage.SupabaseMediaStorage',
    },
    'staticfiles': {
        'BACKEND': 'django_supabase_storage.SupabaseStaticStorage',
    },
}


    and another thing is inside the supabase there is a part at the top of the site that you can change your default database to supabase database for storing the postgre SQL

