"""
Create model to detect spam
"""
import re
m = re.fullmatch(r'(0?[1-9]|1[0-2])/(0?[1-9]|1[0-2])', '10/10')

print(m)