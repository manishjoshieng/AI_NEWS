import json, os


class JsonHandler:
    def __init__(self,filePath) -> None:
        self.filePath = filePath

    def updateFile(self, new_data):
        try:
            with open(self.filePath, "r") as data_file:
                #Reading old data
                old_data = json.load(data_file)
        except:
            with open(self.filePath, "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            #Updating old data with new data
            old_data.update(new_data)
            with open(self.filePath, "w") as data_file:
                #Saving updated data
                json.dump(old_data, data_file, indent=4)

    def removeFile(self):
        try:
            os.remove(self.filePath)
        except:
            print("File not Found on disk")


    def getFile(self):
        try:
            with open(self.filePath, "r") as data_file:
                #Reading old data
                return json.load(data_file)
        except:
            return None