import gzip
from typing import List, Tuple
import zlib
import base64

def preprocess(code: str, replace_list: List[Tuple[str, str]]) -> str:
   for source, target in replace_list:
      code = code.replace(source, target)

   compressed_code = base64.b85encode(zlib.compress(str.encode(code), 9))

   return compressed_code

if __name__ == "__main__":
   code = '''
{{code}}}}
'''[1:-1]

   replace_source = ["vars"]
   replace_target = ['v']

   replace_list = list(replace_source.zip(replace_target))

   compressed_code = preprocess(code, replace_source, replace_target)

   print("Uncompressed:", len(code), "- Compressed:", len(compressed_code))
   print("Code:")
   print(compressed_code)