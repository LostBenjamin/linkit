/*******************************************************************/

// visible led count
#define ANIM_LED_COUNT 64

// standard brightness
#define DEFAULT_BRIGHTNESS_PERCENT 25

// brightness scale for blinking leds in the off state
#define MINIMUM_BRIGHTNESS_SCALE 0.02

/*******************************************************************/

#include "colors.h"
#include "ease.h"
#include "effects.h"
#include "color_math.h"
#include "buffer.h"
#include "fade.h"
#include "render.h"
#include "commands.h"
#include "demo.h"
#include "command_processor.h"
#include "random.h"

RandomSeed<RANDOM_SEED_PIN> randomizer;
CommandProcessor command_processor;
ColorMath color_math;

void setup() { 
  Serial1.begin(115200);  // open internal serial connection to MT7688
  randomizer.randomize();
  reset();
  color_math.setup_colors(false);
  color_math.set_brightness(DEFAULT_BRIGHTNESS_PERCENT);
  erase(true);
  generate_power_ease(POWER_EASE_COUNT, EASE_EXPONENT);
  do_demo();
}

void loop(){ 
  if(command_processor.received_command())
  {
    // resync the effects to a blank state to minimize effects of pausing and restarting
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

