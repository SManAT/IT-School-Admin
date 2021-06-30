import GPUtil
import wmi

"""
A class used to detect the Modell of Hardware
"""


def getSystem():
    c = wmi.WMI()
    my_system = c.Win32_ComputerSystem()[0]
    print(f"Manufacturer: {my_system.Manufacturer}")
    print(f"Model: {my_system. Model}")
    print(f"Name: {my_system.Name}")
    print(f"SystemType: {my_system.SystemType}")
    print(f"SystemFamily: {my_system.SystemFamily}")


def getGPU():
    # GPU information
    gpus = GPUtil.getGPUs()
    list_gpus = []
    for gpu in gpus:
        # name of GPU
        gpu_name = gpu.name
        list_gpus.append((
            gpu_name
        ))

    for gpu in list_gpus:
        print(f"GPU: {gpu}")


def main():
    getSystem()
    getGPU()


if __name__ == "__main__":
    main()
