
void sendtoTCPServer(String p) {
  if (!TCPclient.connected()) {
    Serial.println("Client is not ready");
    return;
  }
  TCPclient.print(p);
}

/*
  *初始化wifi连接
*/
void startSTA() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(wifi_name, wifi_password);
  Serial.print("Wiif is connected");
}

/*
  *初始化和服务器建立连接 :style="value.online?'订阅设备在线':'无订阅设备'"  color:#9A9A9A;
*/
void startTCPClient() {
  if (TCPclient.connect(server_ip, atoi(server_port))) {
    Serial.print("\nConnected to server:");
    Serial.printf("%s:%d\r\n", server_ip, atoi(server_port));

    String tcpTemp = "cmd=1&uid=" + String(UID) + "&topic=" + String(TOPIC) + "\r\n"; //构建订阅指令
    sendtoTCPServer(tcpTemp); //发送订阅指令
    
    preTCPConnected = true;
    preHeartTick = millis();
    TCPclient.setNoDelay(true);
  } else {
    Serial.print("Failed connected to server:");
    Serial.println(server_ip);
    TCPclient.stop();
    preTCPConnected = false;
  }
  preTCPStartTick = millis();
}
