import device

cap_index_list = []
cap_device_list = []

for cap_index, cap_device in enumerate(device.getDeviceList()):
    cap_index_list.append(cap_index)
    cap_device_list.append(f"{cap_index} - {cap_device[0]}")
