import PIL.Image
import PIL.ExifTags
from gmplot import gmplot
from geopy.geocoders import Nominatim
import webbrowser



def extract_exif(img_loc: str) -> dict:
    #open the image
    img = PIL.Image.open(img_loc)

    #get all exif tags in an image
    exif = { 
        PIL.ExifTags.TAGS[k]: v 
        for k, v in img._getexif().items() 
        if k in PIL.ExifTags.TAGS
    }
    return exif

def get_gps_data(exif: dict):
    n = exif['GPSInfo'][2]
    e = exif['GPSInfo'][4]
    lat = ((((n[0] * 60) + n[1]) * 60) + n[2]) / 60 /60 
    long = ((((e[0] * 60) + e[1]) * 60) + e[2]) / 60 /60 
    lat, long = float(lat), float(long)
    return lat, long

def show_gps_data(lat, long):
    gmap = gmplot.GoogleMapPlotter(lat, long, 12)
    gmap.marker(lat, long, "cornflowerblue")
    gmap.draw("location.html")

def get_address_from_gps(lat, long):
    geoloc = Nominatim(user_agent="GetLoc")
    locname = geoloc.reverse(f"{lat}, {long}")
    return locname.address

if __name__ == "__main__":
    img_loc = input("Please input location of image\n=> ")
    exif = extract_exif(img_loc)
    if "GPSInfo" in exif:
        lat, long = get_gps_data(exif)
        print(f"lat: {lat}\nlong: {long}")
        show_gps_data(lat, long)
        address = get_address_from_gps(lat, long)
        print(f"Found address: {address}")
        webbrowser.open("location.html")
    
