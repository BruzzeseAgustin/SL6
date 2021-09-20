import sys, os
# Import Specific MAGIC and CTA parameters 
import lfn2pfn_MAGIC as magic
import lfn2pfn_CTA as cta

def main():
   filepath = sys.argv[1]
   if not os.path.isfile(filepath):
       print("File path {} does not exist. Exiting...".format(filepath))
       sys.exit()
   else:
      file = open(filepath, 'r')
      lines = file.readlines()

      for index, line in enumerate(lines):
          print("Line {}: {}".format(index, line.strip()))
    
      file.close()
  

if __name__ == '__main__':
    main()
