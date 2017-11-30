"""
Utility for unittest
"""

def find_diff_in_dict(dict1, dict2, path=""):
    for key, item in dict1.items():
        if key in dict2:
            dict2_item = dict2.get(key)
            if item == dict2_item:
                pass
            else:
                print(path + "." + key + ": " + "Is Not Same")
            if isinstance(item, dict) and isinstance(dict2_item, dict):
                find_diff_in_dict(item, dict2_item, path + "." + key)
        else:
            print(path + "." + key + ": " + "No Key Match.")