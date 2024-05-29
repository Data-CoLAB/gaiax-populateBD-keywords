import time
import sys
sys.path.append('')
from src.backend.genKeywords import KeywordsGenerator
from src.backend.scrap_CES import scrap_from_url

list_tuple_creds = scrap_from_url('https://ces-v1.lab.gaia-x.eu/credentials-events?page=0&size=1000')

key_gen = KeywordsGenerator()

for (vc_id, id, creds) in list_tuple_creds:
    for credential in creds.get('verifiableCredential', []):
        if credential.get('credentialSubject', {}).get('type') == 'gx:ServiceOffering':
            web_address = credential.get('credentialSubject', {}).get('gx:serviceOffering:webAddress', '')
            title = credential.get('credentialSubject', {}).get('gx:serviceOffering:name','DUMMY TITLE')
            if web_address:
                key_gen.send_to_databases(web_address, id, vc_id, title)
            else:
                print(f"No web address for {id}")

                    