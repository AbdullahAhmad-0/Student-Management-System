import os
def Generate():
    list_of_libFiles = os.listdir('Library_Files')
    list_of_libFiles = [f"Library_Files.{x.replace('.py', '')}" for x in list_of_libFiles if x.endswith('.py')]
    return list_of_libFiles