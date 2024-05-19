const uint16_t *getTemperatureConstant(int temperature) {
  switch (temperature) {
    case 16:
     return TEMP16C;
    case 17:
      return TEMP17C;
    case 18:
      return TEMP18C;
    case 19:
      return TEMP19C;
    case 20:
      return TEMP20C;
    case 21:
      return TEMP21C;
    case 22:
      return TEMP22C;
    case 23:
      return TEMP23C;
    case 24:
      return TEMP24C;
    case 25:
      return TEMP25C;
    case 26:
      return TEMP26C;
    case 27:
      return TEMP27C;
    case 28:
      return TEMP28C;
    case 29:
      return TEMP29C;
    case 30:
      return TEMP30C;
    case 31:
      return TEMP31C;
    case 32:
      return TEMP32C;
    default:
      // 如果温度值不在16到32之间，则返回NULL
      return nullptr;
  }
}

void Operating_airc(int temp) {
  const uint16_t *operate; // 修改为指向 uint16_t 的指针类型

  if (temp == -1) {
    operate = POWEROFF;
    Serial.println("空调开");
  } else if (temp == 0) {
    operate = POWERON;
    Serial.println("空调关");
  } else {  //调温
    operate = getTemperatureConstant(temp);
  }

  // 检查 operate 是否为空指针
  if (operate != nullptr) {
    Serial.println(temp);
    // 使用指针解引用来访问数组中的元素
    Serial.println(operate[1]); // 这里访问数组中的第二个元素
    irsend.sendRaw(operate, ARRAYLENGTH, 38);  // Send a raw data capture at 38kHz.
    delay(2000);
  } else {
    Serial.println("温度值不在16到32之间");
  }
}

