from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import xml.etree.ElementTree as ET
import threading
import requests

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
server = SimpleXMLRPCServer(('localhost', 8000), requestHandler=RequestHandler)
server.register_introspection_functions()

# Database mock: In-memory XML tree.
root = ET.Element("root")

def add_note(topic, text, timestamp):
    for child in root:
        if child.tag == topic:
            new_entry = ET.SubElement(child, "entry", timestamp=timestamp)
            new_entry.text = text
            return True
    new_topic = ET.SubElement(root, topic)
    new_entry = ET.SubElement(new_topic, "entry", timestamp=timestamp)
    new_entry.text = text
    return True

def get_notes(topic):
    for child in root:
        if child.tag == topic:
            return ET.tostring(child, encoding='unicode')
    return "Topic not found."

def delete_entry(topic, timestamp):
    for child in root.findall(topic):
        for entry in child.findall('entry'):
            if entry.get('timestamp') == timestamp:
                child.remove(entry)
                return True
    return False

def delete_topic(topic):
    for child in root.findall(topic):
        root.remove(child)
        return True
    return False

def query_wikipedia(search_term):
    base_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "opensearch",
        "search": search_term,
        "limit": "1",
        "format": "json"
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data[3]:
            return data[3][0]
        return "No article found."
    return "Failed to query Wikipedia."

server.register_function(add_note)
server.register_function(get_notes)
server.register_function(delete_entry)
server.register_function(delete_topic)
server.register_function(query_wikipedia)

def run_server():
    print("Server running on localhost:8000...")
    server.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=run_server).start()
