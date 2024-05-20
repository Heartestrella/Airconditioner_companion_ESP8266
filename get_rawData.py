import os
import re
import time

import serial


class tools:
    def __init__(self) -> None:
        pass

    @staticmethod
    def is_air_conditioning(data: str):
        mesg_desc = {}
        if "Mesg Desc." in data:
            pattern = r"Mesg Desc\.: (.+)"
            matches = re.search(pattern, data)
            if matches:
                mesg_str = matches.group(1)
                key_values = [pair.strip() for pair in mesg_str.split(",")]
                for pair in key_values:
                    key, value = pair.split(":")
                    mesg_desc[key.strip()] = value.strip()

                if "Power" in mesg_desc.keys() and "Temp" in mesg_desc.keys():
                    print(
                        f"可能的空调设备\n电源状态:{mesg_desc['Power']}, 温度:{mesg_desc['Temp']}\n"
                    )
                    return True, mesg_desc
                else:
                    print(mesg_desc, "\n")
                    goon = input(
                        "识别到解析内容，但无法确认为空调设备,是否继续?  Y: 继续 P: 跳过 回答:"
                    )
            else:
                goon = input(
                    f"无法获取到解析内容, 是否继续?  Y: 继续 P: 跳过 回答:"
                ).upper()
        else:
            goon = input("无法确认为空调设备,继续执行?  Y: 继续 P: 跳过 回答:").upper()

        if goon == "YES" or goon == "Y":
            return True, "F"
        elif goon == "P":
            return True, "P"
        return False, None

    @staticmethod
    def get_info(data: str):
        info = {}
        pattern = r"([^:]+)\s*:\s*(.+)"
        matches = re.findall(pattern, data)
        print(f"基本信息:\n")
        for key, value in matches:
            info[key.strip()] = value.strip()
            print(f"{key.strip()}:{value.strip()}")
        print("\n")

    @staticmethod
    def getrawData(data: str):
        pattern_rawData = r"uint16_t rawData\[\d+\] = {(.*?)};"
        match_rawData = re.search(pattern_rawData, data, re.DOTALL)
        if match_rawData:
            rawData_str = match_rawData.group(1)
            rawData_array = [int(num.strip()) for num in rawData_str.split(",")]
            print(f"rawdata: {rawData_array}\n")
            return rawData_array

    @staticmethod
    def read_serial_data():
        buffer = ""
        try:
            while True:
                data = ser.read_until(b";").decode("utf-8")
                buffer += data
                print(data)
                if "uint8_t state" in buffer:
                    return None
                elif buffer.endswith(";"):
                    return buffer
        except KeyboardInterrupt:
            ser.close()
            print("串口关闭")

    @staticmethod
    def create_file_if_not_exists():
        if not os.path.exists("operate.cpp"):
            with open("operate.cpp", "w", encoding="utf-8") as f:
                f.write(
                    '// Operate.cpp\n//This file stores infrared commands \n//Made by Heartestrella\n#include "operate.h"\n'
                )
        if not os.path.exists("operate.h"):
            with open("operate.h", "w", encoding="utf-8") as f:
                f.write(
                    "// Operate.h\n//This file is the header file that defines the operation \n//Made by Heartestrella\n#ifndef CONSTANTS_H\n#define CONSTANTS_H\n#include <cstdint>\nextern const int ARRAYLENGTH;\n"
                )

    @staticmethod
    def wait_for_written(wait_for_written: str, raw_len: int, name: str) -> bool:
        global lened
        if not lened:
            with open("operate.cpp", "a", encoding="utf-8") as f:
                f.write(f"const int ARRAYLENGTH = {raw_len};\n")
            lened = True
        if name not in entered:
            with open("operate.cpp", "a", encoding="utf-8") as f:
                f.write(f"{wait_for_written}\n")
            with open("operate.h", "a", encoding="utf-8") as f:
                f.write(f"extern const uint16_t {name};\n")
            entered.append(name)
            time.sleep(1)
            return True
        else:
            print(f"{name}已经录入了")


if __name__ == "__main__":
    isair = False
    entered = []
    last_temp = 0
    port_ = input("请输入COM端口号: ")
    port = f"COM{port_}"
    baudrate = 115200
    ser = serial.Serial(port, baudrate)
    run = False
    tools.create_file_if_not_exists()
    Unknow_number = 0
    lened = False
    while True:
        data = tools.read_serial_data()
        #  print(data)
        if data:
            run, info = tools.is_air_conditioning(data)
            print("\n")
            if run and info == "P":
                time.sleep(2)
            elif run and info == "F":
                print(f"以兼容模式运行")
                tools.get_info(data)
                rawData = tools.getrawData(data)
                raw_len = len(rawData)
                if isair == False:
                    isair = input("所操作设备是否为空调?").upper()
                if isair == "Y":
                    name_prefix = (
                        input("当前温度(为On或者Off时表示空调开关,请不要输入多余字符)")
                        .upper()
                        .replace(" ", "")
                    )
                    if name_prefix == "ON" or name_prefix == "OFF":
                        name = f"POWER{name_prefix}[{raw_len}]"
                    else:
                        try:
                            int(name)
                        except ValueError as e:
                            print(f"错误的值输入,应该为数字:{name}")
                            print(f"\n错误概括:{e}")
                        name = f"TEMP{name_prefix}[{raw_len}]"
                        wait_for_written = f"const uint16_t {name} = {{{','.join(map(str, rawData))}}};"
                        if wait_for_written:
                            if tools.wait_for_written(wait_for_written, raw_len, name):
                                last_temp = temperature
                                print(f"{name} 录入成功")
                        else:
                            print(f"出现错误 语句不正确:{wait_for_written}")
                else:
                    print("录入未知设备")
                    name = f"UNKOWN{Unknow_number}[{raw_len}]"
                    wait_for_written = (
                        f"const uint16_t {name} = {{{','.join(map(str, rawData))}}};"
                    )
                    if wait_for_written:
                        if tools.wait_for_written(wait_for_written, raw_len, name):
                            print(f"{name} 录入成功")
                    else:
                        print(f"出现错误 语句不正确:{wait_for_written}")
            elif run:
                print(f"以空调模式运行")
                tools.get_info(data)
                rawData = tools.getrawData(data)
                power, temperature = info["Power"], info["Temp"]
                raw_len = len(rawData)
                if power == "Off":
                    name = f"POWEROFF[{raw_len}]"
                    print("Power off 录入")

                elif power == "On" and last_temp == 0:
                    name = f"POWERON[{raw_len}]"
                    print("Power on 录入")

                elif temperature:
                    name = f"TEMP{temperature}[{raw_len}]"
                    print(f"{name} 录入")
                wait_for_written = (
                    f"const uint16_t {name} = {{{','.join(map(str, rawData))}}};"
                )
                if wait_for_written:
                    if tools.wait_for_written(wait_for_written, raw_len, name):
                        last_temp = temperature
                else:
                    print(f"出现错误 语句不正确:{wait_for_written}")
            else:
                import sys

                print("退出")
                sys.exit()
