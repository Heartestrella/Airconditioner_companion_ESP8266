// autohome.ino
// 设置默认参数
// Project by https://github.com/Heartestrella
// 巴法连接逻辑：https://blog.csdn.net/vor234/article/details/121563474
#include <ESP8266WiFi.h>
#include <ESP8266httpUpdate.h>
#include <Arduino.h>
#include <IRremoteESP8266.h>
#include <IRsend.h>
#include "operate.h"

const uint16_t kIrLed = 4;  //红外引脚
IRsend irsend(kIrLed);

#define server_ip "bemfa.com"
#define server_port "8344"
#define UID "你的私钥！"
#define TOPIC "主题名！"  // 会话主题
#define MAX_PACKETSIZE 512
#define KEEPALIVEATIME 30 * 1000
#define wifi_name "wifi名！2,4G的"
#define wifi_password "wifi密码！"
#define upUrl "远程升级固件地址"
WiFiClient TCPclient;
String TcpClient_Buff = "";  //初始化字符串，用于接收服务器发来的数据
unsigned int TcpClient_BuffIndex = 0;
unsigned long TcpClient_preTick = 0;
unsigned long preHeartTick = 0;     //心跳
unsigned long preTCPStartTick = 0;  //连接
bool preTCPConnected = false;
// 基础配置/初始化

//连接WIFI
void doWiFiTick();
void startSTA();

//TCP初始化连接
void doTCPClientTick();
void startTCPClient();
void sendtoTCPServer(String p);

void setup() {
  irsend.begin();
#if ESP8266
  Serial.begin(115200, SERIAL_8N1, SERIAL_TX_ONLY);
#else   // ESP8266
  Serial.begin(115200, SERIAL_8N1);
#endif  // ESP8266
  delay(10);
}

void loop() {
  doWiFiTick();
  doTCPClientTick();
}