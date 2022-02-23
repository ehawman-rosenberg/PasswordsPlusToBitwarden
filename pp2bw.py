import json


def readable_list(seq, sep="and"):
    """Return a grammatically correct human readable string (with an Oxford comma)."""
    # Ref: https://stackoverflow.com/a/53981846/
    seq = [str(s) for s in seq]
    if len(seq) < 3:
        return f' {sep} '.join(seq)
    return ', '.join(seq[:-1]) + f', {sep} ' + seq[-1]


class BitwardenItem():
    # The base item type for Bitwarden

    def __init__(self, type, name, organizationId=None, folderID=None, reprompt=None, notes=None, favorite=False,  collectionIds=None, fields=[]):
        self.type = type
        self.name = name
        self.organizationId = organizationId
        self.folderID = folderID
        self.reprompt = reprompt
        self.notes = notes
        self.favorite = favorite
        self.collectioniDs = collectionIds
        self.fields = fields

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=2)

    def addField(self, fieldDict):
        self.fields.append(fieldDict)


class CustomField():
    # The superclass for Bitwarden custom fields
    # Uses a factory pattern to call subclasses

    type_dict = {
        0: "Text",
        1: "Hidden",
        2: "Boolean",
        3: "Linked"
    }

    def __init__(self, name, type, value=None, linkedId=None):
        self.name = name
        self.value = value
        self.type = type
        self.linkedId = linkedId
        if not isinstance(type, int) or type <= -1 or type >= 4:
            raise ValueError(
                f"A type must be one of {readable_list(CustomField.type_dict.keys(), 'or')}")

    @staticmethod
    def get_field_class_by_type(name, type, value=None, linkedId=None):
        if type == 0 or type == 1:
            return TextOrHiddenCustomField(name, type, value, linkedId)
        elif type == 2:
            return BoolCustomField(name, type, value, linkedId)
        elif type == 3:
            return LinkedCustomField(name, type, value, linkedId)
        else:
            raise Exception("Incorrect type value")

    def __repr__(self):
        return(f"{type(self).__name__}(name: {self.name} | type: {self.type} ({self.type_name()}) | value: {self.value} | linkedID: {self.linkedId})")

    def type_name(self):
        return self.type_dict[self.type]


class TextOrHiddenCustomField(CustomField):
    def __init__(self, name, type, value, linkedId):
        super().__init__(name, type, value, linkedId)
        if not linkedId == None:
            raise Exception("Only a Linked field may have a linkedID")
        if value == None:
            raise Exception(f"A {self.type_dict[type]} field must have a value")


class BoolCustomField(CustomField):
    def __init__(self, name, type, value, linkedId):
        super().__init__(name, type, value, linkedId)
        if not linkedId == None:
            raise Exception("Only a Linked field may have a linkedID")
        if value == None:
            raise Exception(f"A {self.TypeDict[type]} field must have a value")
        if not isinstance(value, bool):
            raise ValueError(f"A Boolean field must have a value of Bool type")


class LinkedCustomField(CustomField):
    def __init__(self, name, type, value, linkedId):
        super().__init__(name, type, value,  linkedId)
        if not value == None:
            raise Exception(
                "A Linked field may only have a linkedId, not a value")
        if linkedId == None:
            raise Exception("A Linked field must have a linkedId")


class URIPattern():
    # A URI and a match type

    match_dict = {
        0: "Default",
        1: "Base domain",
        2: "Host",
        3: "Starts with",
        4: "Regex",
        5: "Exact",
        6: "Never"
    }

    def __init__(self, match, uri):
        self.match = match
        self.uri = uri
        if not isinstance(match, int) or not match in URIPattern.match_dict.keys():
            raise ValueError(
                f"Match must be one of {readable_list(URIPattern.match_dict.keys(), 'or')}")

    def __repr__(self):
        return(f"{type(self).__name__}(Match: {self.match} ({self.match_name()}) | URI: {self.uri}")

    def match_name(self):
        return self.match_dict[self.match]


for i in range(8):
    mytype = i
    mylinkedId = None
    if mytype <=1:
        myvalue = "TESTTEXT"
    elif mytype == 2:
        myvalue = True
    elif mytype == 3:
        myvalue = None
        mylinkedId = "test"
    x = CustomField.get_field_class_by_type(name="myname", type=mytype, value=myvalue, linkedId=mylinkedId)
    print(x)


# {
#     "items": [
#         {
#             "type": 1,
#             "name": "Login Item's Name",
#             "login": {}
#         },
#         {
#             "type": 2,
#             "name": "Secure Note Item's Name",
#             "secureNote": {}
#         },
#         {
#             "type": 3,
#             "name": "Card Item's Name",
#             "card": {}
#         },
#         {
#             "type": 4,
#             "name": "Identity Item's Name",
#             "identity": {}
#         }
#     ]
# }

# {
#     "folders": [
#         {
#             "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
#             "name": "Folder Name"
#         },
#         ...
#     ],
#     "items": [
#         {
#             "id": "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy",
#             "organizationId": null,
#             "folderId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
#             "type": 1,
#             "reprompt": 0,
#             "name": "My Gmail Login",
#             "notes": "This is my gmail login for import.",
#             "favorite": false,
#             "fields": [
#                 {
#                     "name": "custom-field-1",
#                     "value": "custom-field-value",
#                     "type": 0
#                 },
#                 ...
#             ],
#             "login": {
#                 "uris": [
#                     {
#                         "match": null,
#                         "uri": "https://mail.google.com"
#                     }
#                 ],
#                 "username": "myaccount@gmail.com",
#                 "password": "myaccountpassword",
#                 "totp": otpauth: // totp/my-secret-key
#             },
#             "collectionIds": null
#         },
#         ...
#     ]
# }
