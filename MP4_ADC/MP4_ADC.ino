#include <GTimer.h>
#include "AmebaFatFS.h"
#include "StreamIO.h"
#include "VideoStream.h"
#include "MP4Recording.h"

#define TIMER_ID    0
#define ADC_PIN     A0
#define SAMPLE_RATE 2000
#define BUFFER_SIZE 1024


// ---------------- Tiempo ------------
uint32_t length = 30;
uint32_t no_files = 3;


// ---------------- ADC ----------------
volatile int16_t adcBuffer[BUFFER_SIZE];
volatile uint16_t writeIndex = 0;
volatile uint16_t readIndex = 0;

void adcHandler(uint32_t data) {
    adcBuffer[writeIndex] = analogRead(ADC_PIN);
    writeIndex = (writeIndex + 1) % BUFFER_SIZE;
}

// ---------------- SD ----------------
AmebaFatFS fs;
File adcFile;

// ---------------- Video ----------------
#define CHANNEL 0
VideoSetting config(CHANNEL);
MP4Recording mp4;
StreamIO videoStreamer(1,1);

void setup() {

    Serial.begin(115200);
    while (!Serial);

    // --- Iniciar SD ---
    Serial.println("Inicializando SD...");
    if (!fs.begin()) {
        Serial.println("Error iniciando SD");
        while(1);
    }
    String adcPath = String(fs.getRootPath()) + "adc_data.raw";
    adcFile = fs.open(adcPath.c_str());
    if (!adcFile) {
        Serial.println("Error abriendo archivo ADC!");
        while(1);
    }

    // --- Configurar ADC Timer ---
    uint32_t period_us = 1000000UL / SAMPLE_RATE;
    GTimer.begin(TIMER_ID, period_us, adcHandler);
    Serial.println("Muestreo ADC iniciado...");

    // --- Configurar Video ---
    Camera.configVideoChannel(CHANNEL, config);
    Camera.videoInit();

    mp4.configVideo(config);
    mp4.setRecordingDuration(length);
    mp4.setRecordingFileCount(no_files);
    mp4.setRecordingFileName("TestRecordingVideoOnly");
    mp4.setRecordingDataType(STORAGE_VIDEO);

    videoStreamer.registerInput(Camera.getStream(CHANNEL));
    videoStreamer.registerOutput(mp4);
    if (videoStreamer.begin() != 0) {
        Serial.println("StreamIO link start failed");
    }

    Camera.channelBegin(CHANNEL);
    mp4.begin();
    Serial.println("Grabación de video iniciada...");

    analogReadResolution(12);
}

void loop() {
    static uint32_t totalCount = 0;

    // --- Vaciar buffer circular a SD ---
    while (readIndex != writeIndex) {
        int16_t val = adcBuffer[readIndex];
        readIndex = (readIndex + 1) % BUFFER_SIZE;

        adcFile.write((uint8_t*)&val, sizeof(val));
        totalCount++;

        if (totalCount % 1000 == 0) {
            Serial.print("Muestras ADC grabadas: ");
            Serial.println(totalCount);
        }
    }

    adcFile.flush(); // fuerza escritura periódica
}

