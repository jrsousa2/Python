# ALSO INCLUDE PATH IN SETTINGS.JSON SO LINTING DOESN'T DETECT ISSUES
import sys

# adding folder to the system path
sys.path.insert(0, "D:\\Python\\iTunes\\")

# NOT NEEDED IF ADDED TO SETTINGS
import PL_Read # type: ignore

print(sys.path)
