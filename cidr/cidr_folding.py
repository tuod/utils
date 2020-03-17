def fold_networks(network_a, mask_a, network_b, mask_b):
    mask_a = int(mask_a)
    mask_b = int(mask_b)

    def ipv4_str_to_binary(addr):
        bin_addr = 0b1
        for octet in addr.split("."):
            bin_addr <<= 8
            bin_addr |= int(octet)
        return (0b1 << 32) ^ bin_addr

    mask_table = {
        bits: 0b1 << offset for offset, bits in enumerate(reversed(range(33)))
    }

    if mask_a == mask_b:
        binary_ipv4_a = ipv4_str_to_binary(network_a)
        binary_ipv4_b = ipv4_str_to_binary(network_b)
        if binary_ipv4_a + mask_table[mask_a] == binary_ipv4_b:
            return f"{network_a}/{mask_a + 1}"


def get_cidr():
    with open("cidr_rf.txt") as cidr_file:
        return [i.rstrip() for i in cidr_file.readlines()]


def network_fold(arr):
    def foldable(a, b):
        network_a = None
        mask_a = None
        network_b = None
        mask_b = None

        if len(a.split("/")) == 2:
            network_a, mask_a = tuple(a.split("/"))
        if len(b.split("/")) == 2:
            network_b, mask_b = tuple(b.split("/"))
        if network_a and network_b and mask_a and mask_b:
            return fold_networks(network_a, mask_a, network_b, mask_b)

    index = 0
    while len(arr) >= 2 and index + 1 < len(arr):
        fold_result = foldable(arr[index], arr[index + 1])
        if fold_result:
            print(f"{arr[index]} and {arr[index + 1]} folded into {fold_result}")
            arr.pop(index + 1)
            arr[index] = fold_result
            index -= 1 if index else 0
        else:
            index += 1
    return arr


cidr = get_cidr()
start_len = len(cidr)
end_len = len(network_fold(cidr))
print(f"Start length: {start_len}, end length: {end_len}.")

# Кто хочет может сам дописать вывод итогов в файл или куда там вам нужно
