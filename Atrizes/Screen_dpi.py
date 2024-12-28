import ctypes

# Load the necessary libraries
gdi32 = ctypes.WinDLL('gdi32')

def get_dpi():
    # Create a device context for the screen
    hdc = gdi32.GetDC(0)  # 0 is the handle for the screen
    dpi_x = gdi32.GetDeviceCaps(hdc, 88)  # Get the DPI (horizontal)
    dpi_y = gdi32.GetDeviceCaps(hdc, 90)  # Get the DPI (vertical)
    
    # Release the device context
    gdi32.ReleaseDC(0, hdc)
    
    return dpi_x, dpi_y

# Call the function to get DPI
dpi_x, dpi_y = get_dpi()
print(f"Horizontal DPI: {dpi_x}")
print(f"Vertical DPI: {dpi_y}")
