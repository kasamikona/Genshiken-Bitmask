class DSD():
    @staticmethod
    def match_device(device):
        return device.name.startswith("DSD-")
    char_cmd = "d44bc439-abfd-45a2-b575-925416129600"
    char_ack = "d44bc439-abfd-45a2-b575-925416129601"
    char_dat = "d44bc439-abfd-45a2-b575-92541612960a"
    aes_key = "34522A5B7A6E492C08090A9D8D2A23F8"
    width = 48
    height = 12
    monochrome = True
    bitdepth = 1
