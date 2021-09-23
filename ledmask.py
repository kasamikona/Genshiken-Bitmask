import asyncio
import displays

# Update as new displays are added
AUTO_SCAN_CLASSES = [
	displays.DisplayDSD
]
VIRTUAL_CLASSES = [
	displays.DisplayVirtualDSD
]

async def find_and_connect(addresses=None, classes=None, allow_virtual=False):
	print("Looking for compatible display")

	if not classes:
		classes = AUTO_SCAN_CLASSES
		if allow_virtual:
			classes = classes + VIRTUAL_CLASSES

	display = None
	for cls in classes:
		display = await cls.connect(addresses)
		if display:
			print("Found %s" % cls.__name__)
			return display

	print("No display found. Is it switched on and connected?")
	return None
