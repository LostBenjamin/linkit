#ifndef COLORS_H
#define COLORS_H

// eanble to support palettes
// to do: disable palettes
#define USE_PALETTES

#define RED     (*Colors::get_color(Colors::red))
#define ORANGE  (*Colors::get_color(Colors::orange))
#define YELLOW  (*Colors::get_color(Colors::yellow))
#define GREEN   (*Colors::get_color(Colors::green))
#define BLUE    (*Colors::get_color(Colors::blue))
#define PURPLE  (*Colors::get_color(Colors::purple))
#define CYAN    (*Colors::get_color(Colors::cyan))
#define MAGENTA (*Colors::get_color(Colors::magenta))
#define LTBLUE  (*Colors::get_color(Colors::ltblue))
#define LTGREEN (*Colors::get_color(Colors::ltgreen))
#define SEAFOAM (*Colors::get_color(Colors::seafoam))
#define PINK    (*Colors::get_color(Colors::pink))
#define BLACK   (*Colors::get_color(Colors::black))
#define DKGRAY  (*Colors::get_color(Colors::dkgray))
#define GRAY    (*Colors::get_color(Colors::gray))
#define WHITE   (*Colors::get_color(Colors::white))
#define TUNGSTEN (*Colors::get_color(Colors::tungsten))

// tungsten based on 20% brightness, 29,230,255:hsl became 133,70,12
// when unscaled, full strength is 255,135,23, downscaled to 0..20
// is 20,11,2

// to do: consider higher divisor
#define BRIGHTNESS_DIVISOR 20.0
#define NUM_COLORS 17
#define NPRETTY_COLORS 12

#include <PololuLedStrip.h>

const rgb_color color_0 PROGMEM = {20,  0,  0}; // red
const rgb_color color_1 PROGMEM = {20, 10,  0}; // orange
const rgb_color color_2 PROGMEM = {20, 20,  0}; // yellow
const rgb_color color_3 PROGMEM = { 0, 20,  0}; // green
const rgb_color color_4 PROGMEM = { 0,  0, 20}; // blue
const rgb_color color_5 PROGMEM = {10,  0, 20}; // purple
const rgb_color color_6 PROGMEM = { 0, 20, 20}; // cyan
const rgb_color color_7 PROGMEM = {20,  0, 20}; // magenta
const rgb_color color_8 PROGMEM = { 0, 10, 20}; // ltblue
const rgb_color color_9 PROGMEM = {10, 20,  0}; // ltgreen
const rgb_color color_10 PROGMEM = { 0, 20, 10}; // seafoam
const rgb_color color_11 PROGMEM = {20,  0, 10}; // pink
const rgb_color color_12 PROGMEM = { 0,  0,  0}; // black
const rgb_color color_13 PROGMEM = { 5,  5,  5}; // dkgray
const rgb_color color_14 PROGMEM = {10, 10, 10}; // gray
const rgb_color color_15 PROGMEM = {20, 20, 20}; // white
const rgb_color color_16 PROGMEM = {20, 11, 2}; // tungsten

const rgb_color* const color_array[] PROGMEM = {
  &color_0, &color_1,  &color_2,  &color_3,  &color_4,  &color_5,  &color_6,  &color_7,
  &color_8, &color_9, &color_10, &color_11, &color_12, &color_13, &color_14, &color_15,
  &color_16
};

class Colors
{
  public:
  enum color{
    red,
    orange,
    yellow,
    green,
    blue,
    purple,
    cyan,
    magenta,
    ltblue,
    ltgreen,
    seafoam,
    pink,
    black,
    dkgray,
    gray,
    white,
    tungsten
  };

  static const rgb_color * const get_color(color c);

  private:
  // this is pointed-to as the return value for get_color()
  static rgb_color return_color;
};

rgb_color Colors::return_color = {0,0,0};

const rgb_color * const Colors::get_color(color c){
  void *p = (void*)pgm_read_word(&(color_array[c]));
  return_color.red =   pgm_read_byte(p + 0);
  return_color.green = pgm_read_byte(p + 1);
  return_color.blue =  pgm_read_byte(p + 2);
  return &return_color;
}

// unused color combinations
// darkened versions aren't needed because standard ones could be dimmed
//  const rgb_color color_5 PROGMEM = {10, 0, 0}; // dkred
//  const rgb_color color_5 PROGMEM = {10, 10, 0}; // dkyellow
//  const rgb_color color_5 PROGMEM = {0, 10, 0}; // dkgreen
//  const rgb_color color_4 PROGMEM = { 0, 0, 10}; // dkblue
//  const rgb_color color_4 PROGMEM = { 0, 10, 10}; // dycyan
//  const rgb_color color_5 PROGMEM = {10,  0, 10}; // dkmagenta
//
// pale colors look bad
//  const rgb_color color_1 PROGMEM = {20, 10, 10}; // pale red
//  const rgb_color color_2 PROGMEM = {20, 20, 10}; // pale yellow
//  const rgb_color color_9 PROGMEM = {10, 20, 10}; // pale green
//  const rgb_color color_1 PROGMEM = {20, 10, 20}; // pale magenta
//  const rgb_color color_9 PROGMEM = {10, 20, 20}; // pale cyan
//  const rgb_color color_5 PROGMEM = {10, 10, 20}; // pale blue

#endif
