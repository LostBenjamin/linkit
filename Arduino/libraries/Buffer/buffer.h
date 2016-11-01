#ifndef BUFFER_H
#define BUFFER_H

// needs to own the buffers of effects and existence so they can be manipulated
// needs LED_COUNT

#include <PololuLedStrip.h>
#include <render.h>

#define LEAVE_EFFECT -1
#define NO_EFFECT 0

#ifdef EXISTENCE_ENABLED
#define LEAVE_ID -1
#define NO_ID 0
#endif

class Buffer
{
  public:
  PololuLedStripBase *ledStrip;
  rgb_color *buffer;
  static rgb_color *render;
  int *effects;
  float default_brightness_scale;
  Render *renderer;

#ifdef EXISTENCE_ENABLED
  int *existence;
#endif

#ifdef EXISTENCE_ENABLED
  void begin(PololuLedStripBase *ledStrip, int default_brightness, Render *renderer, rgb_color *buffer, rgb_color *render, int *effects, int *existence);
#else
  void begin(PololuLedStripBase *ledStrip, int default_brightness, Render *renderer, rgb_color *buffer, rgb_color *render, int *effects);
#endif

  void display_buffer(rgb_color * pbuffer);
  void erase(bool display);
  void push_color(rgb_color color, bool display, int effect, int max);
  void push_rgb_color(int red, int green, int blue);
  void push_hsl_color(int hue, int sat, int lit);
  void shift(int count, int maxx);
  void finalize_shift(int count, int max);
  void set_color(int pos, rgb_color color, bool display, int effect);
  void set_window(int width);

  private:
  int window;
  void shift_buffer(rgb_color * buffer, int max);
};

rgb_color *Buffer::render;

#ifdef EXISTENCE_ENABLED
void Buffer::begin(PololuLedStripBase *ledStrip, int default_brightness, Render *renderer, rgb_color *buffer, rgb_color *render, int *effects, int *existence){
#else
void Buffer::begin(PololuLedStripBase *ledStrip, int default_brightness, Render *renderer, rgb_color *buffer, rgb_color *render, int *effects){
#endif

  this->ledStrip = ledStrip;
  this->buffer = buffer;
  this->render = render;
  this->default_brightness_scale = default_brightness / 100.0;
  this->effects = effects;

#ifdef EXISTENCE_ENABLED
  this->existence = existence;
#endif

  this->renderer = renderer;
}

void Buffer::display_buffer(rgb_color * pbuffer = render){
  ledStrip->write(pbuffer, ANIM_LED_COUNT);
}
  
void Buffer::erase(bool display = false){
  for(int i = 0; i < ANIM_LED_COUNT; i++){
    buffer[i] = black;
    effects[i] = NO_EFFECT;

#ifdef EXISTENCE_ENABLED
    existence[i] = NO_ID;
#endif
  }

  if(display){
    display_buffer(buffer);
  }
}
  
void Buffer::shift_buffer(rgb_color * buffer, int max = ANIM_LED_COUNT){
  for(int i = max - 1; i >= 1; i--){
    buffer[i] = buffer[i-1];
    effects[i] = effects[i-1];

#ifdef EXISTENCE_ENABLED
    existence[i] = existence[i-1];
#endif

  }
}
  
#ifdef EXISTENCE_ENABLED
void Buffer::push_color(rgb_color color, bool display = false, int effect = NO_EFFECT, int max = 0, int id = NO_ID){
#else
void Buffer::push_color(rgb_color color, bool display = false, int effect = NO_EFFECT, int max = 0){
#endif

  if(max == 0){
    max = (window > 0) ? window : ANIM_LED_COUNT;
  }

  shift_buffer(buffer, max);

  buffer[0] = color;
  effects[0] = effect;

#ifdef EXISTENCE_ENABLED
  existence[0] = id;
#endif

  if(display){
    display_buffer(buffer);
  }
}
  
void Buffer::push_rgb_color(int red, int green, int blue){
  rgb_color color = (rgb_color){red, green, blue};
  color = ColorMath::unscale_color(color, default_brightness_scale);
  push_color(color);
}

void Buffer::push_hsl_color(int hue, int sat, int lit){
  rgb_color color = ColorMath::hsl_to_rgb(hue, sat, lit);
  push_rgb_color(color.red, color.green, color.blue);
}
  
#ifdef EXISTENCE_ENABLED
void Buffer::set_color(int pos, rgb_color color, bool display = false, int effect = NO_EFFECT, int id = NO_ID){
#else
void Buffer::set_color(int pos, rgb_color color, bool display = false, int effect = NO_EFFECT){
#endif
  buffer[pos] = color;
  
  if(effect != LEAVE_EFFECT){
    effects[pos] = effect;
  }

#ifdef EXISTENCE_ENABLED
  if(id != LEAVE_ID){
    existence[pos] = id;
  }
#endif

  if(display){
    display_buffer(buffer);
  }
}
  
void Buffer::set_window(int width){
  if(width < 0){
    width = 0;
  }
  window = width;
}
  
// animate by shifting frame (future: shift in from back buffer)
void Buffer::shift(int count, int maxx = ANIM_LED_COUNT){
  maxx = min(maxx, LED_COUNT);
  for(int i = 0; i < count; i++){
    render[i] = black;
  }
  for(int i = count; i < maxx; i++){
#ifdef USE_FULL_RENDER
    // full render, slower, demo looks worse but looks good in normal operation
    render[i] = renderer->render(buffer[i - count], effects[i - count]);
#else
    render[i] = renderer->fast_render(buffer[i - count], effects[i - count]);
#endif
  }

  display_buffer();
}

void Buffer::finalize_shift(int count, int max){
  for(int i = 0; i < count; i++){
    push_color(black, false, NO_EFFECT, max);
  }
}

#endif

//void draw(rgb_color color, int pos, int id){
//  colors[pos] = ColorMath::add_color(colors[pos], color);
//
//  int mirror = MAX_LED - pos;
//  colors[mirror] = ColorMath::add_color(colors[mirror], color);
//
//  existence[pos] |= bitmask[id];
//}
//
//void undraw(rgb_color color, int pos, int id){
//  existence[pos] &= ~bitmask[id];
//}
