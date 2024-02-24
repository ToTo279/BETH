#include "audio.h"

#include <Arduino.h>
#include <DFPlayerMini_Fast.h>

#include "config.h"
#include "debug.h"

using namespace dfplayer;

Audio::Audio(DFPlayerMini_Fast* DFplayer) {
    DEBUG_PRINTLN("[Audio] Initializing Audio");
    this->player = DFplayer;
    this->player->normalMode();
}

Audio::~Audio() {
    player->stop();
    delete player;
}

void Audio::play(unsigned int track) {
    DEBUG_PRINT("[Audio] Playing track ");
    DEBUG_PRINTLN(track);
    player->play(track);
}

void Audio::pause() {
    DEBUG_PRINTLN("[Audio] Pausing");
    player->pause();
}

void Audio::stop() {
    DEBUG_PRINTLN("[Audio] Stopping");
    player->stop();
}

void Audio::volume(unsigned int volume) {
    DEBUG_PRINT("[Audio] Setting volume to ");
    DEBUG_PRINTLN(volume);
    player->volume(volume);
}

int Audio::readFileCount() {
    DEBUG_PRINTLN("[Audio] Reading file count");
    return player->numSdTracks();
}

void Audio::playStartUpSound() {
    DEBUG_PRINTLN("[Audio] Playing startup sound");
    player->play(STARTUP_SOUND);
}

bool Audio::isPlaying() {
    return player->isPlaying();
}