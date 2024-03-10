from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import xml.etree.ElementTree as ET
from socketserver import ThreadingMixIn
import requests

# Make the server multithreaded
class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

def create_server():
    server = ThreadedXMLRPCServer(('localhost', 8000), requestHandler=RequestHandler)
    server.register_introspection_functions()

    # Mock in-memory XML database
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

    server.register_function(add_note, 'add_note')

    def get_notes(topic):
        for child in root:
            if child.tag == topic:
                return ET.tostring(child, encoding='unicode')
        return "Topic not found."

    server.register_function(get_notes, 'get_notes')

    def delete_entry(topic, timestamp):
        for child in root.findall(topic):
            for entry in child.findall('entry'):
                if entry.get('timestamp') == timestamp:
                    child.remove(entry)
                    return True
        return False

    server.register_function(delete_entry, 'delete_entry')

    def delete_topic(topic):
        for child in root.findall(topic):
            root.remove(child)
            return True
        return False

    server.register_function(delete_topic, 'delete_topic')

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

    server.register_function(query_wikipedia, 'query_wikipedia')

    print("Server running on localhost:8000...")
    server.serve_forever()

if __name__ == "__main__":
    create_server()
