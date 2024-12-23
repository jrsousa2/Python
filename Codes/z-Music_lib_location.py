import ctypes
from ctypes import wintypes

# Define constants
FOLDERID_Music = '{4BD8D571-6D19-48D3-BE97-422220080E43}'

# Convert the string GUID to a ctypes GUID
class GUID(ctypes.Structure):
    _fields_ = [
        ('Data1', wintypes.DWORD),
        ('Data2', wintypes.WORD),
        ('Data3', wintypes.WORD),
        ('Data4', wintypes.BYTE * 8)
    ]

def convert_string_to_guid(guid_string):
    guid = GUID()
    ctypes.windll.ole32.CLSIDFromString(ctypes.c_wchar_p(guid_string), ctypes.byref(guid))
    return guid

def Music_folder():
    # Initialize SHGetKnownFolderPath
    SHGetKnownFolderPath = ctypes.windll.shell32.SHGetKnownFolderPath
    SHGetKnownFolderPath.argtypes = [ctypes.POINTER(GUID), wintypes.DWORD, wintypes.HANDLE, ctypes.POINTER(ctypes.c_wchar_p)]
    SHGetKnownFolderPath.restype = ctypes.HRESULT

    # Convert the string GUID to a ctypes GUID
    guid_music = convert_string_to_guid(FOLDERID_Music)

    # Retrieve the path
    path_ptr = ctypes.c_wchar_p()
    result = SHGetKnownFolderPath(ctypes.byref(guid_music), 0, None, ctypes.byref(path_ptr))

    if result == 0:
        music_folder = path_ptr.value
        print("Music folder path:", music_folder)
    else:
        print("Failed to retrieve the Music folder path. Error code:", result)

Music_folder()