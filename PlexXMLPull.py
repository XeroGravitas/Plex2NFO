import xml.etree.ElementTree as ET
from datetime import datetime, timezone

def generate_audit_log(input_xml, output_txt):
    # Open output file natively in UTF-8
    with open(output_txt, 'w', encoding='utf-8') as out_file:
        first = True
        
        # iterparse streams the XML without loading the whole file into RAM
        context = ET.iterparse(input_xml, events=('end',))
        
        for event, elem in context:
            if elem.tag == 'Video':
                movie_title = elem.get('title')
                year = elem.get('year')
                title_sort = elem.get('titleSort')
                original_title = elem.get('originalTitle')
                added_at = elem.get('addedAt')
                view_count = elem.get('viewCount')
                last_viewed_at = elem.get('lastViewedAt')
                guid = elem.get('guid')
                
                # Defensive type casting for timestamps
                added_at_date = None
                if added_at and added_at.lstrip('-').isdigit():
                    added_at_date = datetime.fromtimestamp(int(added_at), timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                    
                last_viewed_date = None
                if last_viewed_at and last_viewed_at.lstrip('-').isdigit():
                    last_viewed_date = datetime.fromtimestamp(int(last_viewed_at), timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

                part_element = elem.find(".//Part")
                file_path = part_element.get('file') if part_element is not None else "No file path"

                collection_elements = elem.findall(".//Collection")
                collection_tags = [col.get('tag') for col in collection_elements if col.get('tag')]
                collections = ", ".join(collection_tags) if collection_tags else None

                if not first:
                    out_file.write("\n")
                first = False

                # Write directly to disk
                out_file.write(f"Movie Title: {movie_title}\n")
                if year:
                    out_file.write(f"  Year: {year}\n")
                if guid:
                    out_file.write(f"  Plex GUID: {guid}\n")
                if title_sort:
                    out_file.write(f"  TitleSort: {title_sort}\n")
                if original_title:
                    out_file.write(f"  OriginalTitle: {original_title}\n")
                if added_at_date:
                    out_file.write(f"  AddedAt: {added_at_date}\n")
                if last_viewed_date:
                    out_file.write(f"  LastViewedAt: {last_viewed_date}\n")
                if view_count:
                    out_file.write(f"  ViewCount: {view_count}\n")
                if collections:
                    out_file.write(f"  Collections: {collections}\n")
                out_file.write(f"  File Path: {file_path}\n")

                # Clear element to free memory
                elem.clear()

if __name__ == "__main__":
    generate_audit_log('metadata.xml', 'audit_log.txt')