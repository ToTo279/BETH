#ifndef AUDIO_H
#define AUDIO_H

#include <Arduino.h>
#include <DFPlayerMini_Fast.h>
#include "config.h"

using namespace dfplayer;

class Audio
{
public:
    DFPlayerMini_Fast* player;
    Audio(DFPlayerMini_Fast* DFplayer);
    ~Audio();
    void play(unsigned int track);
    void volume(unsigned int volume);
    void stop();
    void pause();
    int readFileCount();
    void playStartUpSound();
    bool isPlaying();
};

#endif