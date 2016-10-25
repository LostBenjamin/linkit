
#include <PololuLedStrip.h>
#include <random_seed.h>

// standard brightness
#define DEFAULT_BRIGHTNESS_PERCENT 25
#include <auto_brightness.h>

#include <color_math.h>
#include <colors.h>

// visible led count
#define ANIM_LED_COUNT 64


// brightness scale for blinking leds in the off state
#define MINIMUM_BRIGHTNESS_SCALE 0.02

#include "ease.h"
#include "effects.h"

#define DATA_OUT_PIN 12 // data out pin for sending color data to the LEDs
#include "buffer.h"

#include "fade.h"
#include "render.h"
#include "commands.h"
#include "demo.h"
#include "command_processor.h"

#define RANDOM_SEED_PIN A1 // floating pin for seeding the RNG
#define LIGHT_SENSOR_PIN A0 // photocell pin for auto-brightness setting

PololuLedStrip<DATA_OUT_PIN> ledStrip;
RandomSeed<RANDOM_SEED_PIN> randomizer;
AutoBrightness<LIGHT_SENSOR_PIN> auto_brightness;
CommandProcessor command_processor;

void setup() { 
  Serial1.begin(115200);  // open internal serial connection to MT7688
  randomizer.randomize();
  reset();
  ColorMath::setup_colors(false);
  ColorMath::set_brightness(DEFAULT_BRIGHTNESS_PERCENT);
  erase(true);
  generate_power_ease(POWER_EASE_COUNT, EASE_EXPONENT);
  do_demo();
}

void loop(){ 
  if(command_processor.received_command())
  {
    // resync the effects to a blank state to minimize visual artifacts of pausing and restarting
    reset_effects();
    
    command_processor.dispatch_command();
  }
  else 
  {
    // process the effects and update the display if needed
    if(process_effects())
      flush();
  }
}

