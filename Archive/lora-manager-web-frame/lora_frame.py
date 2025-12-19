import server

class LoraWebFrame:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {}}

    RETURN_TYPES = ()
    FUNCTION = "do_nothing"
    CATEGORY = "utils"

    def do_nothing(self):
        return ()