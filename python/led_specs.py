#!/usr/bin/python

# ideas: flash green or red depending on tests when done
#        arg to run a single test

import serial 
import time
import sys
import inspect

def get_line_number(back):
  callerframerecord = inspect.stack()[back]    # 0 represents this line, 1 represents line at caller                                                                                                                       
  frame = callerframerecord[0]                                                                                                                                                                  
  info = inspect.getframeinfo(frame)                                                                                                                                                            
  return info.lineno  

#def print_frame():
#  callerframerecord = inspect.stack()[1]    # 0 represents this line
#                                            # 1 represents line at caller
#  frame = callerframerecord[0]
#  info = inspect.getframeinfo(frame)
#  print info.filename                       # __FILE__     -> Test.py
#  print info.function                       # __FUNCTION__ -> Main
#  print info.lineno                         # __LINE__     -> 13

response_wait = 0.1
s = None                                                     
debug_mode = False  
num_tests = 0
num_failures = 0
test_number = 0                                                                                                   
test_description = None                                                                                           
test_failures = []                                                                                                
test_command = None                                                                                               
success_count = 0                                                                                                 
failure_count = 0                                                                                                 
group_number = 0                                                                                                  
group_description = None  
test_line_num = 0
num_pending = 0
last_group_number = 0                                                  
last_test_number = 0 
num_skipped = 0
default_brightness = None                                                                                                                                                              
default_brightness_percent = None                                                                                                                                                  
color_divisor = 20.0                                                                                                                                                                                     
standard_seed = 1
num_groups = 0
test_failure_summaries = []

def flush_input():                        
  s.flushInput()
                                        
def wait_for_ack():                       
  while s.inWaiting() <= 0:               
    pass
  time.sleep(response_wait);
  while s.inWaiting() > 0:
    s.read(s.inWaiting()),

def wait_for_int():
  while s.inWaiting() <= 0:
    pass
  time.sleep(response_wait);
  intstr = ""
  while s.inWaiting() > 0:
    intstr = intstr + s.read(s.inWaiting())
  try:
    return int(intstr[:-1])
  except ValueError:
    print "whoops " + intstr
    return 0

def wait_for_str():
  while s.inWaiting() <= 0:
    pass
  time.sleep(response_wait);
  str = ""
  while s.inWaiting() > 0:
    str = str + s.read(s.inWaiting())
  return str[:-1]

def command(cmd_text):
  global test_command
  test_command = cmd_text
  s.write((cmd_text + ':').encode())
  wait_for_ack()

def command_int(cmd_text):
  s.write((cmd_text + ':').encode())
  return wait_for_int()

def command_str(cmd_text):       
  s.write((cmd_text + ':').encode()) 
  return wait_for_str()                     

def set_macro(macro, macro_text):
  print "macro " + str(macro) + ": ",
  bytes = command_int(str(macro) + ":set:" + macro_text)
  print str(bytes) + " bytes"
  if debug_mode:                                             
    print command_str("1," + str(macro) + ":tst")

def setup(): 
  global s, debug_mode, num_leds, default_brightness, default_brightness_percent 
  s = serial.Serial("/dev/ttyS0", 115200) 
  command(":::stp:stp:20:lev")
  num_leds = command_int("0,0:tst")                                                                                                                                                        
  default_brightness = command_int("0,4:tst")                                                                                                
  default_brightness_percent = default_brightness / 100.0                                                                                                               

  print cyan("Device: ") + white(str(num_leds) + " LEDs, default brightness: " + str(default_brightness) + "%")                                                                                                                                                  

#  if len(sys.argv) > 3:                                       
#    if(sys.argv[3] == "debug"):
#      debug_mode = True

colors = [
  ("red", "20,0,0"),
  ("org", "20,10,0"),
  ("yel", "20,20,0"),
  ("grn", "0,20,0"),
  ("blu", "0,0,20"),                                             
  ("pur", "10,0,20"),                                             
  ("cyn", "0,20,20"),                                             
  ("mag", "20,0,20"),                                             
  ("lbl", "0,10,20"),                                             
  ("lgr", "10,20,0"),                                             
  ("sea", "0,20,10"),                                             
  ("pnk", "20,0,10"),                                             
  ("amb", "20,15,0"),                                             
  ("olv", "15,20,0"),                                             
  ("sky", "0,15,20"),                                             
  ("tur", "0,20,15"),                                             
  ("lav", "15,0,20"),                                             
  ("ros", "20,0,15"),                                             
  ("blk", "0,0,0"),                                             
  ("dgr", "5,5,5"),                                             
  ("gry", "10,10,10"),                                             
  ("wht", "20,20,20"),                                             
  ("tun", "20,11,2")                                             
]

def write(text):
  sys.stdout.write(text)
  sys.stdout.flush()                                                

def black(text):
  return "\x1b[30m" + text + normal()

def red(text):
  return "\x1b[31m" + text + normal()

def green(text):                                              
  return "\x1b[32m" + text + normal()

def yellow(text):
  return "\x1b[33m" + text + normal()            

def blue(text):                            
  return "\x1b[34m" + text + normal()  

def magenta(text):                            
  return "\x1b[35m" + text + normal()  

def cyan(text):
  return "\x1b[36m" + text + normal()

def white(text):                                                   
  return "\x1b[37m" + text + normal()                             

def normal():                             
  return "\x1b[39m"                                     

def black(text):                                                                                                                           
  return "\x1b[40m" + text + normal()                                                                                                                

def redbg(text):                                   
  return "\x1b[41m" + text + normalbg()                   
                                                        
def greenbg(text):                                        
  return "\x1b[42m" + text + normalbg()                   
                                                 
def yellowbg(text):                                       
  return "\x1b[43m" + text + normalbg()            
                                                        
def bluebg(text):                                         
  return "\x1b[44m" + text + normalbg()                   
                                                        
def magentabg(text):                               
  return "\x1b[45m" + text + normalbg()                   
                                                        
def cyanbg(text):                            
  return "\x1b[46m" + text + normalbg()                   
                                                        
def whitebg(text):                         
  return "\x1b[47m" + text + normalbg()                   
                                                        
def normalbg():                                          
  return "\x1b[49m"  

num_leds = 0

def group(description):                                                                    
  global group_number, group_description, last_group_number, num_groups
  group_number = group_number + 1
  num_groups += 1
  group_description = description
  set_standard_seed()                                                                                                                                                                                      

def test(description):
  global test_number, test_description, test_failures, last_test_number
  test_number = test_number + 1
  test_description = description 
  command(":::stp:stp:20:lev")

def report_group():
  global last_group_number
  if group_number != last_group_number:                                                                                                                                                                    
    test_failures.append(cyan("\nGroup #" + str(group_number) + " " + group_description))                                                                                                                    
    last_group_number = group_number                                                       

def report_test():
  global last_test_number
  report_group()
  if test_number != last_test_number:                                                                                                                                                                      
    test_failures.append(blue("  Test #" + str(test_number) + " " + test_description))                                                                                                                     
    last_test_number = test_number                                                      

def report_failure(got, expected):
  report_test()
  test_failures.append("    " + red("Expectation: ") + cyan("[" + test_command + "]") + cyan(" @ " + str(test_line_number)) + red(" Failed!\n") + red("\texpected:\n") + yellow("\t\t[" + expected + "]\n") + red("\tgot:\n") + yellow("\t\t[" + got + "]") + "\n")
  test_failure_summaries.append(cyan("\t@ " + str(test_line_number) + " ") + yellow(test_command) + red(" -" + expected) + green(" +" + got + "\n")) 

def report_pending():
  report_test()
  test_failures.append("    " + yellow("Pending expectation: ") + yellow("[" + test_description + "]") + cyan(" @ " + str(test_line_number))) 

def report_skipped():                                                                                                                                                                                      
  report_test()                                                                                                                                                                                            
  test_failures.append("    " + red("Skipped expectation: ") + red("[" + test_command + "] ") + red("[" + test_description + "]") + cyan(" @ " + str(test_line_number)))                                                             
                                                                                      
def fail(got, expected):
  global test_failures, failure_count, last_group_number, last_test_number
  report_failure(got, expected)
  write(red("F"))
  failure_count += 1
  last_group_number = group_number
  last_test_number = test_number

def pending_test(description):
  global test_number, test_description, test_line_number, num_pending                                                                                                                                                                                  
  test_line_number = get_line_number(2)                                                                                                                                                                    
  test_number = test_number + 1                                                                                                                                                                            
  test_description = description    
  report_pending()
  num_pending += 1
  write(yellow("."))

def skip_test(command, description):
  global test_number, test_description, test_line_number, num_skipped
  test_line_number = get_line_number(2)                                                                                                       
  test_number = test_number + 1                                                                                                                                                                            
  test_description = description                                                                                                                                                                           
  report_skipped()                                                                                                                                                                                         
  num_skipped += 1                                                                                                                                                                                         
  write(red("s"))                                                                                                                          

def succeed():
  global success_count
  write(green("."))
  success_count += 1

def expect_equal(got, expected):
  global test_line_number
  test_line_number = get_line_number(3)
  if got != expected:
    fail(got, expected)
  else:
    succeed()

def expect_buffer(command_, start, count, expected):
  command(command_)
  str_ = command_str("2," + str(start) + "," + str(count) + ":tst")                                 
  expect_equal(str_[:-1], expected)

def expect_render(command_, start, count, expected):               
  command(command_)                                                
  str_ = command_str("3," + str(start) + "," + str(count) + ":tst")
  expect_equal(str_[:-1], expected)                                
                                                                   
def expect_effect(command_, start, count, expected):               
  command(command_)                                                
  str_ = command_str("4," + str(start) + "," + str(count) + ":tst")
  expect_equal(str_[:-1], expected)                                
                                                                   
def expect_palette(command_, start, count, expected):               
  #command(command_)                                                
  #str_ = command_str("5," + str(start) + "," + str(count) + ":tst")
  #expect_equal(str_[:-1], expected)                                
  pass                                                                

def rgb_string(red, green, blue):
  return str(red) + "," + str(green) + "," + str(blue)

def rgb_strings(red, green, blue):
  return str(red) + "," + str(green) + "," + str(blue) + ","

def unscaled_color_value(rgb_color_value):
  return int(((rgb_color_value / default_brightness_percent) / 255) * color_divisor)

def rendered_color_value(buffer_color_value):
  return int(((buffer_color_value / color_divisor) * 255) * default_brightness_percent) 

def set_standard_seed():
  command_str("6,3," + str(standard_seed) + ":tst")

########################################################################
########################################################################

def specs():
  # --------------------------------------------------------------------
  group("pushing colors to display buffer")

  test("it sets a pre-rendered value in the buffer")
  expect_buffer("red", 0, 1, "20,0,0")

  test("it sets an alternate cyan value in the buffer")
  expect_buffer("cyn", 0, 1, "0,20,20") 

  test("it accurately sets all standard colors")
  for color in colors:
    expect_buffer(color[0] + ":flu", 0, 1, color[1])

  # --------------------------------------------------------------------             
  group("pushing multiple colors")                                                                                     
                                                                                                                       
  test("it places two colors (only)")                                                                                  
  expect_buffer("2:yel:flu", 0, 3, "20,20,0,20,20,0,0,0,0")                          

  # it works in reverse mode

  test("it places multiple colors in reverse mode")
  expect_buffer("1:rev:2:sea:flu", 87, 3, "0,0,0,0,20,10,0,20,10")
                                                                                                                       
  # --------------------------------------------------------------------                                               
  group("pause and continue")

  test("it doesn't render while paused")
  expect_render("red", 0, 1, "0,0,0")

  # --------------------------------------------------------------------                                               
  group("rendering colors to the render buffer")

  test("it renders a rendered blue value in the render buffer")
  expect_render("blu:flu", 0, 1, "0,0,51")

  test("it renders an alternate value in the render buffer")
  expect_render("org:flu", 0, 1, "51,25,0")

  # --------------------------------------------------------------------                                               
  group("erasure")

  test("it erases the rendered value")
  expect_render("red:flu", 0, 1, "51,0,0")
  expect_render("era:flu", 0, 1, "0,0,0")

  test("it erases only within the set window")
  expect_render("6:pnk:flu", 0, 6, "51,0,25,51,0,25,51,0,25,51,0,25,51,0,25,51,0,25")
  expect_render("2:off:4:win:era:flu", 0, 6, "51,0,25,51,0,25,0,0,0,0,0,0,51,0,25,51,0,25")

  test("it erases within the set window in reverse mode")
  expect_render("1:rev:6:pnk:flu", 84, 6, "51,0,25,51,0,25,51,0,25,51,0,25,51,0,25,51,0,25")                                                                                                                                                              
  # offset and window are always in reference to pixel 0 regardless of reversal
  expect_render("86:off:88:win:era:flu", 84, 6, "51,0,25,51,0,25,0,0,0,0,0,0,51,0,25,51,0,25") 

  # --------------------------------------------------------------------                                               
  group("repeating")

  test("it repeats the color value only once")
  expect_buffer("grn:rep:flu", 0, 3, "0,20,0,0,20,0,0,0,0")

  # this will break many existing scripts
  # test("it doesn't repeat if arg0 is zero")
  # expect_buffer("olv:0:rep:flu", 0, 2, "15,20,0,0,0,0")

  # repeating works in reverse mode
  pending_test("it repeats properly in reverse mode")
  # expect_buffer("1:rev:gry:rpt:flu", 88, 2, "10,10,10,10,10,10")

  # --------------------------------------------------------------------                                               
  group("flooding")

  test("it floods all leds")
  expected_buffer = ("10,0,20," * num_leds)[:-1]
  expect_buffer("pur:flo:flu", 0, num_leds, expected_buffer)

  test("it floods only within the set window")
  expect_buffer("2:off:4:win:ros:flo:flu", 0, 6, "0,0,0,0,0,0,20,0,15,20,0,15,0,0,0,0,0,0")

  # not sure how to test this
  # pending_test("it does no flooding if there's no room")

  skip_test("1:rev:amb:flo:flu", "it floods properly in reverse mode")
  # expected_buffer = ("20,15,0," * num_leds)[:-1]                                                                                                                                                           
  # expect_buffer("1:rev:amb:flo:flu", 0, num_leds, expected_buffer)  

  # --------------------------------------------------------------------                                               
  group("mirroring")
   
  test("it mirrors the pattern accurately")
  expect_buffer("cyn:yel:mag:mir:flu", 0, 3, "20,0,20,20,20,0,0,20,20")
  expect_buffer("", num_leds - 3, 3, "0,20,20,20,20,0,20,0,20")

  pending_test("it mirrors only within the set window")

  pending_test("it mirrors properly in reverse mode") 

  # --------------------------------------------------------------------                                               
  group("pushing effects to the effects buffer")

  test("it places an effect in the effects buffer")
  expect_effect("org:bli:flu", 0, 1, "10")

  pending_test("it places an alternate effect in the effects buffer")

  pending_test("it places multiple effects in the effects buffer")
 
  # --------------------------------------------------------------------                                               
  group("positioning")

  test("pos sets the next insertion postion and default 0 width")
  expect_buffer("1:pos:red:flu", 0, 3, "0,0,0,20,0,0,0,0,0")

  test("pos sets the offset + width")
  expect_buffer("1,2:pos:wht:flo:flu", 0, 4, "0,0,0,20,20,20,20,20,20,0,0,0")

  test("offset override is always relative to LED #0")
  expect_buffer("2:off:2:off:lav:flu", 0, 5, "0,0,0,0,0,0,15,0,20,0,0,0,0,0,0")

  skip_test("1:rev:3:pos:tun:flo:flu", "positioning works in reverse mode")
  # positioning is always relative to LED #0 and should be unaffected by direction
  # expect_buffer("0:rev:3:pos:tun:flo:flu", 0, 5, "0,0,0,0,0,0,0,0,0,20,11,2,0,0,0")                                                          
  # expect_buffer("1:rev:3:pos:tun:flo:flu", 0, 5, "0,0,0,0,0,0,0,0,0,20,11,2,0,0,0")

  skip_test("1:rev:2,2:pos:lgr:flo:flu", "positioning with width works in reverse mode")
  # expect_buffer("1:rev:2,2:pos:lgr:flo:flu", 0, 4, "")                                                                                                                                  

  # --------------------------------------------------------------------                                               
  group("copying")

  pending_test("it copies the right number of pixels")
  pending_test("it copies the right number of times")
  pending_test("it fills the current width if times is zero")
  pending_test("it copies to the palette buffer if 18 or fewer pixels are being copied")
  pending_test("it copies to the render buffer if more than 18 pixels are being copied")
  pending_test("it overwrites the original position when duplicating")
  pending_test("it copies the right number of zoomed pixels")
  pending_test("it copies a pattern to the palette")
  pending_test("it pastes a pattern to the buffer")
  pending_test("it pastes the pattern at the current offset")
 
  # --------------------------------------------------------------------                                                                                                                                   
  group("palette manipulation")                                                            

  pending_test("the palette defaults to a fixed set of colors")
  pending_test("the palette can be shuffled")
  pending_test("the shuffler creates alternating complimentary colors")
  pending_test("the shuffler creates complimentary colors for the current palette")
  pending_test("the shuffler creates random complimentary colors")
  pending_test("the shuffler resets to the original fixed set of colors")

  # --------------------------------------------------------------------                                                                  
  group("zones")                                                                          

  pending_test("choosing a zone sets the offset and window")
  pending_test("choosing the main zone resets to 0, num_leds")
                                                                                                                                                                                                            
  # --------------------------------------------------------------------                                                                  
  group("setting offset and window")                                                                          
                                                              
  pending_test("an offset can be set")
  pending_test("the next pushed color is inserted at the offset")
  pending_test("a window can be set")
  pending_test("pushed-off-the-end colors don't exceed the window boundary")
  pending_test("setting an offset if relative to the current offset")
  pending_test("an offset outside the current window cannot be set")
                                                                                                                                             
  # --------------------------------------------------------------------                                                                  
  group("reverse and forward")                                                                          
          
  pending_test("the insertion mode can be set to reverse")
  pending_test("the insertion mode can be set to normal")

  # --------------------------------------------------------------------                                                                  
  group("rgb color")                                                                          

  color_value = 255
  unscaled_color_value_ = unscaled_color_value(color_value)
  rendered_color_value_ = rendered_color_value(unscaled_color_value_)

  # compute pre-rendered value for full-brightness pixel
  expected_rgb_color = rgb_string(unscaled_color_value_, unscaled_color_value_, unscaled_color_value_)

  test("it unscales to the proper pre-rendered value")
  expect_buffer("255,255,255:rgb:flu", 0, 1, expected_rgb_color)

  # compute rendered value for recovered full-brightness pixel
  expected_render_value = rendered_color_value_
  expected_rgb_color = rgb_string(expected_render_value, expected_render_value, expected_render_value)

  test("it renders the expected RGB value in the render buffer")                                                                                                        
  # must render at default brightness to recover the original value
  expect_render(str(default_brightness) + ":lev:255,255,255:rgb:flu", 0, 1, expected_rgb_color)                                                         

  test("current brightness level doesn't affect unscaling calculation")
  expect_render("1:lev:255,255,255:rgb:" + str(default_brightness) + ":lev:flu", 0, 1, expected_rgb_color)                         
                                                                  
  # --------------------------------------------------------------------                                                                  
  group("hsl color")                                                                          

  color_value = 255                                                                         
  unscaled_color_value_ = unscaled_color_value(color_value)                                                                                                                                                
  rendered_color_value_ = rendered_color_value(unscaled_color_value_)                                                                                                                                      
                                                         
  test("it sets the expected HSL value in the display buffer")                                                                                                                                     
  expected_rgb_color = str(unscaled_color_value_) + ",0,0"
  expect_buffer("0,255,255:hsl:flu", 0, 1, expected_rgb_color)

  test("it renders the expected HSL value in the render buffer")                                                                                                                                   
  expected_rgb_color = str(rendered_color_value_) + ",0,0"                                                                                                                                                 
  expect_render(str(default_brightness) + ":lev:0,255,255:hsl:flu", 0, 1, expected_rgb_color)                                                                                                          
                
  test("current brightness level doesn't affect unscaling calculation")                                                                                                                                    
  expect_render("1:lev:0,255,255:hsl:" + str(default_brightness) + ":lev:flu", 0, 1, expected_rgb_color)
                                                                                                                                    
  # --------------------------------------------------------------------                                                                  
  group("custom black level")                                                                          
  
  pending_test("a custom black level can be set")
  pending_test("erases uses the custom black level")
  pending_test("placing 'black' uses the custom black level")
                                                                                                                                                                                                         
  # --------------------------------------------------------------------                                                                  
  group("random color")                                                                          
                                                             
  test("it chooses a random color")
  expect_buffer("rnd:flu", 0, 1, "15,20,0")  

  test("it chooses another random color")
  expect_buffer("rnd:flu", 0, 1, "20,0,20")                                                                                                                                 

  test("it sets no effect")
  expect_effect("rnd:flu", 0, 1, "0")

  test("it repeats using the same color not another random color")               
  expect_buffer("rnd:rep:flu", 0, 2, "20,20,0,20,20,0")  

  test("it floods using the same color not another random color")
  expect_buffer("rnd:flo:flu", 0, 2, "0,0,20,0,0,20")

  test("it sets a random color and sets the effect to repeat with random colors")
  expect_buffer("1:rnd:flu", 0, 1, "0,10,20")                                                                                        
  expect_effect("1:rnd:flu", 0, 1, "1")  

  test("it repeats using a different color")
  expect_buffer("1:rnd:rep:flu", 0, 2, "20,0,15,0,10,20")

  test("it floods using a different color each time")                                                                                                                                                      
  expect_buffer("1:rnd:flo:flu", 0, 3, "20,10,0,20,0,0,20,0,15") 

  test("the repeated colors get no effect set")
  expect_effect("1:rnd:rep:rep:flu", 0, 3, "0,0,1") 

  test("the flooded colors get no effect set")                          
  expect_effect("1:rnd:flo:flu", 0, 3, "1,0,0")    

  test("it sets a random color and sets the effect to repeat with random colors+effects")                                                                                                                          
  expect_buffer("2:rnd:flu", 0, 1, "20,20,0")                                                                                                                                                                    
  expect_effect("2:rnd:flu", 0, 1, "2") 

  test("it repeats using a different color")                                                                                                                                                               
  expect_buffer("2:rnd:rep:flu", 0, 2, "20,20,0,0,20,0")                                                                                                              
                                                                                                                                                                                                           
  test("it floods using a different color each time")                                                 
  expect_buffer("2:rnd:flo:flu", 0, 3, "15,0,20,10,0,20,20,15,0")                                                                                                                                          

  test("the flooded colors get random effects set")                                     
  expect_effect("2:rnd:flo:flu", 0, 3, "2,14,21") 

  test("the repeated colors get random effects set")                                                                                                                                                            
  expect_effect("2:rnd:rep:rep:flu", 0, 3, "0,0,2")                                                                                                                                                        

  # --------------------------------------------------------------------                                                                  
  group("blending colors")                                                                          
                                                                                                                                                                                                           
  # --------------------------------------------------------------------                                                                  
  group("max, dim and bright")                                                                          
                                                                                                                                                                                                           
  # --------------------------------------------------------------------                                                                  
  group("blink effects")                                                             
                                                                                                                                                                                                           
  # --------------------------------------------------------------------                                                                  
  group("breathe effect")                                                             
                                                                                                                                                                                                           
  # --------------------------------------------------------------------                                                                  
  group("fade and twinkle effects")                                                             
                                                                                                                                                                                                           
  # --------------------------------------------------------------------                                                                  
  group("raw effect")                                                             
                                                                                                                                                                                                           
  # --------------------------------------------------------------------                                                                  
  group("reset, clear and stop")                                                             
                                                                                                                                                                                                           
  # --------------------------------------------------------------------                                                                  
  group("brightness level")                                                             
                                                                                                                                                                                                           
  # --------------------------------------------------------------------                                                                  
  group("fade animation")                                                             
                                                                                                                                                                                                           
  # --------------------------------------------------------------------                                                                  
  group("wipe animation")                                                             
                                                                                                                                                                                                           
  # --------------------------------------------------------------------                                                                  
  group("animated rotation")                                                             
                                                                                                                                                                                                           
  # --------------------------------------------------------------------                                                                  
  group("rotation")                                                             
                                                                                                                                                                                                           
  # --------------------------------------------------------------------                                                                  
  group("power shift")                                                             
                                                                                                                                                                                                           
  # --------------------------------------------------------------------                                                                  
  group("crossfade")                                                             
                                                                                                                                                                                                           
  # --------------------------------------------------------------------                                                                  
  group("setting fade rate")                                                             
                                                                                                                                                                                                           
  # --------------------------------------------------------------------                                                                  
  group("setting custom blink period")                                                             
                                                                                                                                                                                                           
  # --------------------------------------------------------------------                                                                  
  group("setting blink period")                                                             
                                                                                                                                                                                                           
  # --------------------------------------------------------------------                                                                  
  group("carry color")                                                                                                            
                                                                                                                                                                                                           
  # --------------------------------------------------------------------                                                                  
  group("setting custom breathe time")                                                                                                            
                                                                                                                                                                                                           
  # --------------------------------------------------------------------                                                                  
  group("setting and running macros")                                                                                                            
                                                                                                                                                                                                           
  # --------------------------------------------------------------------                                                                  
  group("delay")                                                                                                            
                                                                                                                                                                                                           
  # --------------------------------------------------------------------                                                                  
  group("random number")                                                                                                            
                                                                                                                                                                                                           
  # --------------------------------------------------------------------                                                                  
  group("position")                                                                                                            
                                                                                                                                                                                                           
  # --------------------------------------------------------------------                                                                  
  group("random postion")                                                                                                            
                                                                                                                                                                                                           
  # --------------------------------------------------------------------                                                                  
  group("sequencing")                                                                                                            
                                                                                                                                                                                                           
  # --------------------------------------------------------------------                                                                  
  group("testing")                                                                                                            
                                                                                                                                                                                                           
########################################################################                     
########################################################################                     
 
def loop():                                  
  print
  specs()
  test("")
  print 

  for error in test_failures:
    print error

  if(failure_count > 0):
    print red("Failures:")
    for summary in test_failure_summaries:                                                                                                                                                                              
      print summary,

  print
  print blue(str(num_groups) + " groups ") + cyan(str(success_count + failure_count) + " expectations ") + green(str(success_count) + " succeeded ") + red(str(failure_count) + " failed ") + yellow(str(num_pending) + " pending ") + red(str(num_skipped) + " skipped")                                                                      
  print                                                                                                                                                                                            


if __name__ == '__main__': 
  print magenta("\nApollo Lighting System Test Framework v0.0\n")
  setup() 
  loop()
  print

