import asyncio
import displays

AUTO_SCAN_CLASSES = [ # Update as new displays are added
	displays.DisplayDSD
]

async def find_and_connect(classes=None, addresses=None):
	print("Looking for compatible display")

	if not classes:
		classes = AUTO_SCAN_CLASSES

	display = None
	for cls in classes:
		display = await cls.connect(addresses)
		if display:
			print("Found %s" % cls.__name__)
			return display

	print("No display found. Is it switched on and connected?")
	return None
