
import os
from supabase import create_client, Client
from dotenv import load_dotenv
load_dotenv()   

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

#Getting number from database
def get_number(plate):
    try:
        #FIXME: to be changed to the actual table name
        response = supabase.table('vehicles').select('*').eq("plate",plate).execute()
        data= response.data[0]
        print(data)
        return {"contact":data['contact'],'owner':data['owner'], 'plate':data['plate'],'fine':data['fine'],'charge':data['charge']}
    
    except Exception as e:
        print("Error: ",e)
        return None
    

#NOTE: This is just for testing purposes

#Adding item to database
# def add_item():
#     try:
#         data = supabase.table('vehicles').insert([{'owner': 'Swetank', 'contact': 7761878881,'plate':'SWETANK'}]).execute()
#         print(data)
#         return data
#     except Exception as e:
#         print("Error: ",e)
#         return None

def fine(plate:str):
    #update the value of the column charge by adding 1000 to the existing value
    try:
        #get the current value of the charge column
        response = supabase.table('vehicles').select('charge').eq('plate',plate).execute()
        data = response.data[0]
        charge = data['charge']
        
        #update the value of the charge column
        response = supabase.table('vehicles').update({'charge':charge+1000}).eq('plate',plate).execute()
        print(response)
        return response
    except Exception as e:
        print("Error: ",e)
        return None
