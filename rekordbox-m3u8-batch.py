import xml.etree.ElementTree as ET
import os
import re

def sanitize_filename(name):
    """Replace bad characters with spaces."""
    return re.sub(r'[\\/*?:"<>|]', ' ', name)

def get_track_info(collection, track_key):
    """Get track information from the COLLECTION using the track key."""
    track = collection.find(f"./TRACK[@TrackID='{track_key}']")
    if track is not None:
        title = track.get('Name')
        artist = track.get('Artist')
        location = track.get('Location')
        duration = track.get('TotalTime')

        # Extract file path from 'Location'
        if location:
            if location.startswith('file://localhost/'):
                location = location[17:]  # Remove 'file://localhost/' prefix
            elif location.startswith('file://'):
                location = location[7:]  # Remove 'file://' prefix
            location = location.replace('%20', ' ')  # Replace URL encoded spaces with actual spaces
        
        return artist, title, location, duration
    return None, None, None, None

def process_playlist_node(node, collection, base_path=""):
    playlist_name = node.get('Name')
    node_type = node.get('Type')

    if not playlist_name:
        return

    # Sanitize the playlist name to be used as a filename or folder name
    sanitized_playlist_name = sanitize_filename(playlist_name)

    # If the node is a folder (Type 0) and not the ROOT node, create a directory and recurse into child nodes
    if node_type == "0" and playlist_name != "ROOT":
        new_base_path = os.path.join(base_path, sanitized_playlist_name)
        os.makedirs(new_base_path, exist_ok=True)
        for child_node in node.findall('NODE'):
            process_playlist_node(child_node, collection, new_base_path)
    # If the node is a playlist (Type 1), create an M3U8 file
    elif node_type == "1":
        playlist_filename = os.path.join(base_path, f"{sanitized_playlist_name}.m3u8")
        with open(playlist_filename, 'w', encoding='utf-8') as m3u8:
            m3u8.write("#EXTM3U\n")

            for track_entry in node.findall('./TRACK'):
                track_key = track_entry.get('Key')
                artist, title, location, duration = get_track_info(collection, track_key)

                if location and duration:
                    m3u8.write(f"#EXTINF:{duration},{artist} - {title}\n")
                    m3u8.write(f"{location}\n")

        print(f"M3U8 playlist created successfully: {playlist_filename}")

    # If the node is the ROOT node, process its child nodes directly
    elif node_type == "0" and playlist_name == "ROOT":
        for child_node in node.findall('NODE'):
            process_playlist_node(child_node, collection, base_path)

def rekordbox_xml_to_m3u8(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    collection = root.find('COLLECTION')
    if collection is None:
        print("No COLLECTION element found in the XML file.")
        return

    playlists = root.find('PLAYLISTS')
    if playlists is None:
        print("No PLAYLISTS element found in the XML file.")
        return

    output_dir = "playlists"
    os.makedirs(output_dir, exist_ok=True)

    for node in playlists.findall('NODE'):
        process_playlist_node(node, collection, output_dir)

# Example usage:
rekordbox_xml_to_m3u8('rekordbox.xml')
