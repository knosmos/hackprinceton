#include <Arduino.h>
#include <pgmspace.h> // For PROGMEM support
#include <TFT_eSPI.h> // Fast ESP32 TFT library
// #include <Adafruit_GFX.h> // Include the Adafruit GFX library
// #include <Adafruit_GC9A01A.h> // Include the Adafruit GC9A1 library
#include <ESP32Servo.h> // Servo interfacing library
#include <SPI.h> // Include SPI library for communication with the display
#include <bitmaps.h>

// Adafruit_GC9A01A::Adafruit_GC9A01A(int8_t cs, int8_t dc, int8_t mosi,
//     int8_t sclk, int8_t rst, int8_t miso)
// 15, 2, 13, 14, -1, -1

#define TFT_CS   15 // Chip select pin
#define TFT_DC   2  // Data/Command pin
TFT_eSPI tft = TFT_eSPI();
TFT_eSprite b = TFT_eSprite(&tft);
uint16_t *scr;

// Color definitions
#define BLACK    0x0000
#define BLUE     0x001F
#define RED      0xF800
#define GREEN    0x07E0
#define CYAN     0x07FF
#define MAGENTA  0xF81F
#define YELLOW   0xFFE0 
#define WHITE    0xFFFF

// buffer
uint16_t *buffer;
uint16_t _width, _height;

// class Buffer :public Adafruit_GFX {
// public:
//     Buffer(int16_t w, int16_t h) : Adafruit_GFX(w, h) {
//         _width = w;
//         _height = h;
//         buffer = (uint16_t *)malloc(w * h * sizeof(uint16_t));
//         memset(buffer, 0, w * h * sizeof(uint16_t));
//     }

//     ~Buffer() {
//         free(buffer);
//     }

//     void drawPixel(int16_t x, int16_t y, uint16_t color) {
//         if ((x >= 0) && (x < _width) && (y >= 0) && (y < _height)) {
//             buffer[x + y * _width] = color;
//         }
//     }

//     uint16_t* getBuffer() {
//         return buffer;
//     }
// };

Servo servo;

void setup() {
    Serial.begin(115200);
    tft.begin();
    tft.setRotation(0); // Set rotation if needed
    scr = (uint16_t*)b.createSprite(240, 240);
    servo.attach(12);
    servo.write(30);
    // b.fillScreen(WHITE); // Clear the screen with white color
    // b.setTextColor(BLACK); // Set text color to black
    // b.setTextSize(10); // Set text size
    // b.setCursor(0, 0); // Set cursor position
    // b.println("Hello, World!"); // Print a message to the display

    // b.drawBitmap(100, 100, epd_bitmap_blob, 64, 64, BLACK); // Draw the bitmap at (0, 0)

    // tft.setAddrWindow(0, 0, 240, 240);
    // digitalWrite(TFT_DC, HIGH);
    // digitalWrite(TFT_CS, LOW);
    // SPI.beginTransaction(SPISettings(80000000, MSBFIRST, SPI_MODE0));
    //    for (uint16_t i = 0; i < 240*240; i++)
    //    {
    //       SPI.write16(buffer[i]);
    //    }
    // SPI.endTransaction();
    // digitalWrite(TFT_CS, HIGH);

    // print display buffer
    // for (int i=0; i<240; i++){
    //     for (int j=0; j<240; j++){
    //         Serial.print(buffer[i*240+j], HEX);
    //         Serial.print(" ");
    //     }
    //     Serial.println("");
    // }
}

char c = '1';
int servoState = 0;
void loop() {
    // b.fillScreen(BLUE); // Clear the screen with white color
    // Serial.println("sleep_1");
    // b.drawBitmap(88, 88, epd_bitmap_sleep_1, 64, 64, WHITE); // Draw the bitmap at (0, 0)
    // delay(100); // Just a delay for demonstration purposes
    // Serial.println("sleep_2");
    // b.fillScreen(BLUE); // Clear the screen with white color
    // b.drawBitmap(88, 88, epd_bitmap_sleep_2, 64, 64, WHITE); // Draw the bitmap at (0, 0)
    // delay(100); // Just a delay for demonstration purposes
    
    // read from serial
    if (Serial.available()) {
        c = Serial.read();
        servo.write(30);
    }

    if (c == '1') {
        Serial.println("sleeping");
        b.fillScreen(TFT_BLUE);
        b.drawBitmap(0, 0, epd_bitmap_resized_sleep_1, 240, 240, TFT_WHITE);
        b.pushSprite(0, 0);
        delay(200);
        b.fillScreen(TFT_BLUE);
        b.drawBitmap(0, 0, epd_bitmap_resized_sleep_2, 240, 240, TFT_WHITE);
        b.pushSprite(0, 0);
        delay(200);
    }
    else if (c == '2') {
        Serial.println("awake");
        b.fillScreen(TFT_BLUE);
        b.drawBitmap(0, 0, epd_bitmap_resized_awake_1, 240, 240, TFT_WHITE);
        b.pushSprite(0, 0);
        delay(200);
        b.fillScreen(TFT_BLUE);
        b.drawBitmap(0, 0, epd_bitmap_resized_awake_2, 240, 240, TFT_WHITE);
        b.pushSprite(0, 0);
        delay(200);
    }
    else if (c == '3') {
        Serial.println("annoyed_1");
        b.fillScreen(TFT_BLUE);
        b.drawBitmap(0, 0, epd_bitmap_resized_annoyed_1, 240, 240, TFT_WHITE);
        b.pushSprite(0, 0);
        servo.write(60);
        delay(200);
        b.fillScreen(TFT_BLUE);
        b.drawBitmap(0, 0, epd_bitmap_resized_annoyed_2, 240, 240, TFT_WHITE);
        b.pushSprite(0, 0);
        servo.write(0);
        delay(200);
    }
    else if (c == '4') {
        Serial.println("annoyed_2");
        b.fillScreen(TFT_BLUE);
        b.drawBitmap(0, 0, epd_bitmap_resized_touchgrass_1, 240, 240, TFT_WHITE);
        b.pushSprite(0, 0);
        servo.write(60);
        delay(200);
        b.fillScreen(TFT_BLUE);
        b.drawBitmap(0, 0, epd_bitmap_resized_touchgrass_2, 240, 240, TFT_WHITE);
        b.pushSprite(0, 0);
        servo.write(0);
        delay(200);
    }
    else if (c == '5') {
        Serial.println("dead");
        b.fillScreen(TFT_BLUE);
        b.drawBitmap(0, 0, epd_bitmap_resized_dead_1, 240, 240, TFT_WHITE);
        b.pushSprite(0, 0);
        delay(200);
        b.fillScreen(TFT_BLUE);
        b.drawBitmap(0, 0, epd_bitmap_resized_dead_2, 240, 240, TFT_WHITE);
        b.pushSprite(0, 0);
        delay(200);
    }
}