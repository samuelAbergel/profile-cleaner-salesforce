import sys
import re
import xml.etree.ElementTree as ET
import os

def namespace(element):
  return re.match(r'\{.*\}', element.tag).group(0)

def profiles_cleaner(profile_file):
  tree = ET.parse(profile_file)
  root = tree.getroot()
  ns = namespace(root)
  ET.register_namespace('', ns[1:-1])
  packages = ('AAKCS', 'Field_Trip', 'ELEE', 'archanaanndev', 'bcmanhelp', 'fsLtng', 'sortablegrid', 'due', 'fluent_commerce', 'alcmeon', 'Alcmeon', 'Twilio', 'TwilioSF', 'OdigoSms', 'Odigo', 'orgcheck', 'analyticsengine', 'Profile2PermSet', 'Jigsaw', 'DuplicateRecordItem', 'DuplicateRecordSet', 'LiveAgentSession', 'LiveChatTranscript', 'LiveChatVisitor', 'Location', 'MessagingEndUser', 'MessagingSession', 'ServiceResource', 'SocialPersona', 'SocialPost', 'p0pFD', 'FlowOrchestrationInstance', 'FlowOrchestrationWorkIte', 'MessagingChannel', 'SessionHijackingEventStore', 'Field_Trip', 'DidUEnjo')

  removedObjects = []
  removedRecordTypes = []

  aplicationPath = find_metadata_path_folder(common_path, sfoa_path, 'applications')
  for application in root.findall(ns + 'applicationVisibilities'):
    visible = application.find(ns + 'visible')
    applicationText = application.find(ns + 'application')
    if (visible.text == 'false') or (applicationText is not None and any(package in applicationText.text for package in packages)):
        root.remove(application)
    elif not existing_metadata_in_repository(aplicationPath, applicationText.text, 'app'):
        root.remove(application)

  classesPath = find_metadata_path_folder(common_path, sfoa_path, 'classes')
  for apexClass in root.findall(ns + 'classAccesses'):
    enabled = apexClass.find(ns + 'enabled')
    apexClassText = apexClass.find(ns + 'apexClass')
    if (enabled.text == 'false') or (apexClassText is not None and any(package in apexClassText.text for package in packages)):
      root.remove(apexClass)
    elif not existing_metadata_in_repository(classesPath, apexClassText.text, 'cls'):
        root.remove(apexClass)

  customMetadataList = find_metadata_path_folder(common_path, sfoa_path, 'objects')
  for customMetadata in root.findall(ns + 'customMetadataTypeAccesses'):
    enabled = customMetadata.find(ns + 'enabled')
    customMetadataText = customMetadata.find(ns + 'name')
    if (enabled.text == 'false') or (customMetadataText is not None and any(package in customMetadataText.text for package in packages)):
        root.remove(customMetadata)
    elif not existing_metadata_in_repository(customMetadataList, customMetadataText.text, 'object'):
        root.remove(customMetadata)

  for customSetting in root.findall(ns + 'customSettingAccesses'):
    enabled = customSetting.find(ns + 'enabled')
    customSettingText = customSetting.find(ns + 'name')
    if (enabled.text == 'false') or (customSettingText is not None and any(package in customSettingText.text for package in packages)):
        root.remove(customSetting)

  for externalDataSource in root.findall(ns + 'externalDataSourceAccesses'):
    enabled = externalDataSource.find(ns + 'enabled')
    if (enabled.text == 'false'):
      root.remove(externalDataSource)

  fieldsMetadata = find_metadata_path_folder(common_path, sfoa_path, 'fields')
  for field in root.findall(ns + 'fieldPermissions'):
    readable = field.find(ns + 'readable')
    fieldText = field.find(ns + 'field')
    fieldTextAfterDot = fieldText.text.split('.', 1)[1] if '.' in fieldText.text else None
    if (readable.text == 'false') or (fieldText is not None and any(package in fieldText.text for package in packages)):
      root.remove(field)
    elif not existing_metadata_in_repository(fieldsMetadata, fieldTextAfterDot, 'field'):
        root.remove(field)

  for flow in root.findall(ns + 'flowAccesses'):
    enabled = flow.find(ns + 'enabled')
    if (enabled.text == 'false'):
      root.remove(flow)

  objectMetadata = find_metadata_path_folder(common_path, sfoa_path, 'objects')
  for object in root.findall(ns + 'objectPermissions'):
    allowRead = object.find(ns + 'allowRead')
    objectText = object.find(ns + 'object')
    if (allowRead.text == 'false') or (objectText is not None and any(package in objectText.text for package in packages)):
      root.remove(object)
      removedObjects.append(object.find(ns + 'object').text)
    elif not existing_metadata_in_repository(objectMetadata, objectText.text, 'object'):
      root.remove(object)
      removedObjects.append(object.find(ns + 'object').text)

  pageMetadata = find_metadata_path_folder(common_path, sfoa_path, 'pages')
  for apexPage in root.findall(ns + 'pageAccesses'):
    enabled = apexPage.find(ns + 'enabled')
    apexPageText = apexPage.find(ns + 'apexPage')
    if (enabled.text == 'false') or (apexPageText is not None and any(package in apexPageText.text for package in packages)):
      root.remove(apexPage)
    elif not existing_metadata_in_repository(pageMetadata, apexPageText.text, 'page'):
      root.remove(apexPage)

  recordTypeMetadata = find_metadata_path_folder(common_path, sfoa_path, 'recordTypes')
  for recordType in root.findall(ns + 'recordTypeVisibilities'):
    visible = recordType.find(ns + 'visible')
    recordTypeText = recordType.find(ns + 'recordType')
    recordTypeAfterDot = recordTypeText.text.split('.', 1)[1] if '.' in recordTypeText.text else None
    if (visible.text == 'false') or (recordTypeText is not None and any(package in recordTypeText.text for package in packages)):
      root.remove(recordType)
      removedRecordTypes.append(recordType.find(ns + 'recordType').text)
    elif not existing_metadata_in_repository(recordTypeMetadata, recordTypeAfterDot, 'recordType'):
      root.remove(recordType)
      removedRecordTypes.append(recordType.find(ns + 'recordType').text)

  tabMetadata = find_metadata_path_folder(common_path, sfoa_path, 'tabs')
  for tab in root.findall(ns + 'tabVisibilities'):
    visibility = tab.find(ns + 'visibility')
    tabText = tab.find(ns + 'tab')
    if (visibility.text == 'Hidden') or (tabText is not None and any(package in tabText.text for package in packages)):
      root.remove(tab)
    elif not existing_metadata_in_repository(tabMetadata, tabText.text, 'tab'):
      root.remove(tab)

  layoutMetadata = find_metadata_path_folder(common_path, sfoa_path, 'layouts')
  for layout in root.findall(ns + 'layoutAssignments'):
    recordType = layout.find(ns + 'recordType')
    layoutText = layout.find(ns + 'layout')
    if (recordType is None and layout.find(ns + 'layout').text.partition('-')[0] in removedObjects):
        root.remove(layout)
    elif (recordType is not None and recordType.text in removedRecordTypes):
        root.remove(layout)
    elif layoutText is not None and any(package in layoutText.text for package in packages):
        root.remove(layout)
    elif not existing_metadata_in_repository(layoutMetadata, layoutText.text, 'layout'):
      root.remove(layout)

  tree.write(profile_file, encoding='utf-8', xml_declaration=True)
  print(profile_file)

def find_metadata_path_folder(common_path, sfoa_path, metadata_name):
    metadata_paths = []
    for root, dirs, _ in os.walk(common_path):
        if metadata_name in dirs:
            metadata_paths.append(os.path.join(root, metadata_name))
    for root, dirs, _ in os.walk(sfoa_path):
        if metadata_name in dirs:
            metadata_paths.append(os.path.join(root, metadata_name))
    return metadata_paths

def existing_metadata_in_repository(possible_paths, metadata_name, end_file_path):
    if end_file_path == 'object':
        return any(os.path.exists(path + '\\' + metadata_name + '\\' + metadata_name + '.' + end_file_path +  '-meta.xml') for path in possible_paths)
    return any(os.path.exists(path + '\\' + metadata_name + '.' + end_file_path +  '-meta.xml') for path in possible_paths)

if __name__ == '__main__':
  common_path = 'common-app'
  sfoa_path = 'sfoa-app'
  profile_path = 'PROFILES\\profilesAll'
  for root, dirs, files in os.walk(profile_path):
    for file in files:
      if file.endswith('.profile-meta.xml'): 
        profile_file_path = os.path.join(root, file)
        profiles_cleaner(profile_file_path) 
