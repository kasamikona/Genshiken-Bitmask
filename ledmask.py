import asyncio, threading
import displays

# Update as new displays are added
AUTO_SCAN_CLASSES = [
	displays.DisplayDSD
]

async def find_and_connect(addresses=None, classes=None, dispargs=None):
	print("Looking for compatible display")

	if not classes:
		print("No classes specified")
		return None

	display = None
	for cls in classes:
		display = await cls.connect(addresses, dispargs)
		if display:
			print("Found %s" % cls.__name__)
			return display

	print("No display found. Is it switched on and connected?")
	return None
