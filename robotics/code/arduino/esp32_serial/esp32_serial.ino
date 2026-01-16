#include <WiFi.h>
#include <esp_wifi.h>

// Structure to hold captured data safely
struct PacketData {
  uint8_t mac[6];
  char ssid[33];
  bool pending = false;
};

volatile PacketData lastPacket; // Shared between callback and loop

void sniffer(void* buf, wifi_promiscuous_pkt_type_t type) {
  if (type != WIFI_PKT_MGMT) return; 

  wifi_promiscuous_pkt_t *pkt = (wifi_promiscuous_pkt_t*)buf;
  uint8_t* payload = pkt->payload;

  // Filter for Probe Requests (Subtype 0x04)
  if ((payload[0] & 0xFC) == 0x40) {
    // Copy MAC and SSID to our global storage instead of printing
    memcpy((void*)lastPacket.mac, &payload[10], 6);
    
    int len = payload[25];
    if (len > 0 && len <= 32) {
      memcpy((void*)lastPacket.ssid, &payload[26], len);
      lastPacket.ssid[len] = '\0';
      lastPacket.pending = true; // Signal the loop to print
    }
  }
}

void setup() {
  Serial.begin(115200); // Standard speed is more stable for debugging
  delay(2000); 

  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  
  esp_wifi_set_promiscuous(true);
  esp_wifi_set_promiscuous_rx_cb(&sniffer);
  esp_wifi_set_channel(1, WIFI_SECOND_CHAN_NONE);
  
  Serial.println("\n--- STABLE SNIFFER INITIALIZED ---");
}

void loop() {
  // Check if a new packet was captured by the sniffer
  if (lastPacket.pending) {
    Serial.printf("MAC: %02X:%02X:%02X:%02X:%02X:%02X | SSID: %s\n", 
                  lastPacket.mac[0], lastPacket.mac[1], lastPacket.mac[2], 
                  lastPacket.mac[3], lastPacket.mac[4], lastPacket.mac[5], 
                  lastPacket.ssid);
    
    lastPacket.pending = false; // Clear the flag
  }

  // Automatic channel hopping
  static unsigned long lastHop = 0;
  static int ch = 1;
  if (millis() - lastHop > 10000) {
    ch = (ch % 13) + 1;
    esp_wifi_set_channel(ch, WIFI_SECOND_CHAN_NONE);
    lastHop = millis();
    Serial.printf(">>> Switched to Channel %d\n", ch);
  }
}
