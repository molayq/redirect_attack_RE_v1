import random
import string
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import time
from urllib.parse import urlparse

import requests

def check_attack():
    rootUrl = 'https://rrgrocery.co/v-l-b/?n6CsGQcyl-HCLPsh'
    attackRootRequest = requests.get(
        rootUrl,
        allow_redirects=True, verify=False)
    # print(page.url)
    # print(page.status_code)
    # print(page.raw)
    pagePossibleRedirect = attackRootRequest.url
    print('##### -> Redirect through a phishing page ->', pagePossibleRedirect)
    ####check if the redirect was made
    pageHistory = ''
    for response in attackRootRequest.history:
        print('##### -> Before redirect through a phishing page ->', response.url)

        pageHistory = response.url
        rollOver = '##### -> Pages kept the same.' \
            if pagePossibleRedirect == response.url else '##### -> Mare muie. Redirect was made'
        print(rollOver)
    ####check for active attack
    responseCodeToInt = int(attackRootRequest.status_code)
    if (responseCodeToInt == 404):
        print("##### -> Safe for now. No active attack. Page was disabled")
    elif responseCodeToInt > 200 and responseCodeToInt < 399:
        print("##### -> Response code of the page indicates an active attack.")

    ####check if its another domain in the redirect
    domainFromRootUrl = urlparse(rootUrl).netloc
    domainFromHistory = urlparse(pageHistory).netloc
    isAnotherDomain = '##### -> The same domain used in the attack' \
        if domainFromRootUrl == domainFromHistory else '##### -> Another domain was used in the redirect'
    print(isAnotherDomain)


    ######check if there is another attack still active on the domain
    ###check only the query param on the URI --- keep /v-l-b/ as reference subroot
    ###traverse from the query param and see if a 200 is received on a redirect
    #referenceUri =  'https://rrgrocery.co/v-l-b/?n6CsGQcyl-HCLPsh'
start = time()
def reverseTraversal():
    #for traverseIndex in range(10):
    # keep the length and format of query string, without numbers
    randomSix = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=6))
    exampleUrlConcatenated = 'https://rrgrocery.co/v-l-b/?n6CsGQcyl-%s' % randomSix

    reverseTraversalAttack = requests.get(
        exampleUrlConcatenated,
        allow_redirects=True)
    print('Traversal in reverse ->>> %s -url:  %s' % (reverseTraversalAttack.status_code,  reverseTraversalAttack.url))
    #print(traverseIndex)


check_attack()

processes = []
with ThreadPoolExecutor(max_workers=14) as executor:
    for x in range(10):
        processes.append(executor.submit(reverseTraversal))

#reverseTraversal()

# for task in as_completed(processes):
#     print(task.result())
print(f'Time taken: {time() - start}')