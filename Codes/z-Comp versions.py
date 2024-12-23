import win32com.client

# General approach, automatically uses the latest version
iTunesApp_general = win32com.client.Dispatch("iTunes.Application")

# Specific approach, targets a specific version
iTunesApp_specific = win32com.client.Dispatch("iTunes.Application.1")

# Verify that both approaches can interact with the iTunes application
print(f"General approach version: {iTunesApp_general.Version}")
print(f"Specific approach version: {iTunesApp_specific.Version}")
