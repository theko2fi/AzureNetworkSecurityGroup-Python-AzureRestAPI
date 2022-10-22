# importing the requests library
import requests, json

tenantId = "bbXXXXXX-XXXX-XXXX-XXXX-XXXXXXXX"
client_id = "d2XXXXXX-XXXX-XXXX-XXXX-XXXXXXXX"
client_secret = "XXXX~XXXX~XXXXXXXXXXXXXXXX"
subscriptionId = "b6XXXX-XXXX-XXXX-XXXX-XXXXXXXX"

resourceGroupName = "test-az-nsg-api-RG"
securityRuleName = "AllowAnyHTTPInbound"
networkSecurityGroupName = "test-api-vm-nsg"


def getToken():
  # api-endpoint
  URL = "https://login.microsoftonline.com/{}/oauth2/token".format(tenantId)
  data = "grant_type=client_credentials&client_id={}&client_secret={}&subscriptionId={}&resource=https%3A%2F%2Fmanagement.azure.com%2F".format(client_id, client_secret, subscriptionId)
  # sending get request and saving the response as response object
  r = requests.post(url = URL, data = data)
  # extracting data in json format
  result = r.json()
  #return the token value
  return result['access_token']

def apiCall(data):
  URL = "https://management.azure.com/subscriptions/{}/resourceGroups/{}/providers/Microsoft.Network/networkSecurityGroups/{}/securityRules/{}?api-version=2022-05-01".format(subscriptionId,resourceGroupName,networkSecurityGroupName,securityRuleName)
  headers = {
    "Authorization": "Bearer " + getToken(),
    "Content-Type": "application/json",
    "dataType": "json"
  }
  r = requests.put(url = URL, headers=headers, data=json.dumps(data))
  print(r.json())


if __name__ == "__main__":

  #define the NSG security rule properties
  securityRuleProperties = {
  "properties": {
    "description": "Allow inbound traffic from Something",
    "protocol": "TCP",
    "sourcePortRange": "*",
    "destinationPortRange": "425",
    "sourceAddressPrefix": "192.168.46.1",
    "destinationAddressPrefix": "10.201.100.4",
    "access": "Allow",
    "priority": 1051,
    "direction": "Inbound"
    }
  }

  #call the API
  apiCall(securityRuleProperties)

