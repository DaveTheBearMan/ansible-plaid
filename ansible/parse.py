#!/usr/bin/env python3
import yaml
import re

class ANSI():
    def background(code):
        return "\33[{code}m".format(code=code)

    def style_text(code):
        return "\33[{code}m".format(code=code)

    def color_text(code):
        return "\33[{code}m".format(code=code)

def GetHostData(Host, FixedLength=True):
	# Always return a list in case inventory has hosts in [X:X] format
	HostList = []

	# Check for [X:X] format on host
	HostRegex = re.search("[0-9]+:[0-9]+", Host)
	if HostRegex:
		# Split string in order to add index for each host
		MatchingRange = HostRegex.group()
		StringHalves = Host.split('[' + MatchingRange + ']')

		IndexRange = MatchingRange.split(':')
		BeginIndex = int(IndexRange[0])
		EndIndex = int(IndexRange[1])
		for Index in range(BeginIndex, EndIndex):
			# Whether or not we need to pad the host with zeros
			HostNumber = str(Index) if not FixedLength else str(Index).zfill(len(IndexRange[-1]))
			HostList.append(StringHalves[0] + HostNumber + StringHalves[1])
	else:
		HostList.append(Host)
	return HostList

def FlattenDictToListAndKeepDictionaries(Dictionary):
	FlattenedList = []

	for Key, Value in Dictionary.items():
		if isinstance(Value, dict):
			FlattenedList.append(Value)
		else:
			FlattenedList.append(Key)

	return FlattenedList

def UnpackHosts(HostList, Hosts):
	MatchingHosts = []

	for Host in HostList:
		if isinstance(Host, dict):
			if 'children' in Host:
				FlattenedList = FlattenDictToListAndKeepDictionaries(Host['children'])
				MatchingHosts.extend(UnpackHosts(FlattenedList, Hosts)) # Holy fuck Bobby, it's recursion!
			else:
				raise IndexError("Hostlist with no children but is a dictionary: " + Host)
		else:
			MatchingHosts.extend(Hosts[Host])

	return MatchingHosts

if __name__ == '__main__':
	with open("test_inventory.yaml", "r") as file:
		inventory = yaml.safe_load(file)

	Hosts = {}
	for host, data in inventory['all']['children'].items():
		if 'children' in data: continue
		# First host only
		Hosts[host] = GetHostData(list(data['hosts'])[0])

	Groups = {}
	for Group, Data in inventory['all']['children'].items():
		if 'children' not in Data: continue
		print(list(Data['children']))

		# If there are any recursive groups in a group with children ##listed##, this will catch them
		# This will not catch groups inside of groups, that functionality does not yet exist
		FlattenedList = FlattenDictToListAndKeepDictionaries(Data['children'])
		print(f"\nProvided List for {Group}:", FlattenedList)
		Groups[Group] = UnpackHosts(FlattenedList, Hosts)
		print(ANSI.background(34) + f"\nFinal List for {Group}:")
		print(Groups[Group])

	print(Groups)
