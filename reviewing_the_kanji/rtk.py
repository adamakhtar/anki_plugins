# Automatically adds Reviewing The Kanji stories for Kanji to cards
# Requires two fields named as Expression and Heisig
# Expression has the source text. Heisig will have stories inserted by the plugin
# Expression must have two astericks around the kanji you want to have stories searched for
# E.g. blah blah *some kanji* blah blah

import re
import json
from anki.hooks import addHook

def onFocusLost(flag, n, fidx):
    rtkStoriesPath = '/Users/adam/Documents/Anki/addons/rtk.json'
    from aqt import mw
    # japanese model?
    expression = None
    heisig = None
    definition = None

    if "rtk" not in n.model()['name'].lower():
        return flag
    # have src and dst fields?
    for c, name in enumerate(mw.col.models.fieldNames(n.model())):
        if name == 'Expression':
            expression = name
            expressionIndex = c
        if name == 'Heisig':
            heisig = name
            heisigIndex = c


    # event coming from src field?
    if fidx != expressionIndex:
        return flag
    # grab source text
    if not expression or not heisig:
        return flag
    # dst field already filled?
    if n[heisig]:
        return flag
    expressionText = mw.col.media.strip(n[expression])
    if not expressionText:
        return flag
    # update field
    try:
        match = re.search('\*(.*?)\*',expressionText)

        if match is None:
            return flag

        with open(rtkStoriesPath, 'r') as stream:
            rtk_definitions = json.load(stream)
            # match = re.search('\*(.*?)\*',expressionText)
            focusText = match.group(1)
            storiesString = ""
            for character in list(focusText):
                item = next((item for item in rtk_definitions if item["kanji"] == character), None)
                if not item:
                    continue

                if item:
                    storiesString += "<p>"
                    storiesString += ("<strong>" + item['kanji'] + "</strong>")
                    storiesString += " - "
                    storiesString += ("<em>" + item['keyword'] + "</em>")
                    storiesString += ' - '
                    storiesString += item['story']
                    storiesString += "</p>"
                else:
                    continue

            n[heisig] = storiesString
    except Exception, e:
        raise e
    return True

addHook('editFocusLost', onFocusLost)




# import re
# import json
# from anki.hooks import addHook

# def onFocusLost(flag, n, fidx):
#     rtkStoriesPath = '/Users/adam/Documents/Anki/addons/rtk.json'
#     from aqt import mw
#     # japanese model?
#     expression = None
#     heisig = None
#     definition = None

#     if "rtk" not in n.model()['name'].lower():
#         raise NameError("1")
#         return flag
#     # have src and dst fields?
#     for c, name in enumerate(mw.col.models.fieldNames(n.model())):
#         if name == 'Expression':
#             expression = name
#             expressionIndex = c
#         if name == 'Heisig':
#             heisig = name
#             heisigIndex = c
#         if name == 'Definitions':
#             definition = name
#             definitionIndex = c


#     # event coming from src field?
#     if fidx != expressionIndex:
#         return flag
#     # grab source text
#     if not expression or not heisig or not definition:
#         raise NameError(list(enumerate(mw.col.models.fieldNames(n.model()))))
#         return flag
#     # dst field already filled?
#     if n[definition] or n[heisig]:
#         return flag
#     expressionText = mw.col.media.strip(n[expression])
#     if not expressionText:
#         raise NameError("5")
#         return flag
#     # update field
#     try:
#         with open(rtkStoriesPath, 'r') as stream:
#             rtk_definitions = json.load(stream)
#             match = re.search('\*(.*?)\*',expressionText)
#             focusText = match.group(1)
#             storiesString = ""
#             for character in list(focusText):
#                 if not rtk_definitions.has_key(character):
#                     raise NameError(character, rtk_definitions, focusText +"here", expressionText)
#                     continue
#                 story = rtk_definitions[character]


#                 if story:
#                     storiesString += character
#                     storiesString += " - "
#                     storiesString += story
#                 else:
#                     # raise NameError("7")
#                     continue

#             n[heisig] = storiesString
#     except Exception, e:
#         raise e
#     return True

# addHook('editFocusLost', onFocusLost)