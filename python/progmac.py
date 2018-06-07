#!/usr/bin/python

import serial 
import time
import sys
import terminal_colors as tc
import led_command as lc
import argparse
import app_ui as ui
import macro_compiler as mc

global app_description, verbose_mode, debug_mode, legacy_mode, num_leds, macro_count, program, macro_run_number, presets, dryrun, bytes_programmed, show_output
app_description = None
verbose_mode = None
debug_mode = None
legacy_mode = None
macro_count = 0
num_leds = None
programs = None
macro_run_number = None
presets = None
dryrun = None
bytes_programmed = None
show_output = None

def get_options():
    global verbose_mode, debug_mode, program, macro_run_number, starting_macro, num_macro_chars, ending_macro, number_of_sequencer, presets, dryrun, show_output

    parser = argparse.ArgumentParser(description=app_description)
    parser.add_argument("program", help="program to transmit")
    parser.add_argument("presets", nargs="*", help="resolved=value presets (None)")
    parser.add_argument("-m", "--macro", type=int, dest="macro", default=10, help="macro number to run after programming (10)")
    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true", help="display verbose info (False)")
    parser.add_argument("-d", "--debug", dest="debug", action="store_true", help="display verbose info (False)")
    parser.add_argument("-l", "--legacy", dest="legacy", action="store_true", help="use legacy .mac file format (False)")
    parser.add_argument("-r", "--dryrun", dest="dryrun", action="store_true", help="process the script but don't actually program the device (False)")
    parser.add_argument("-o", "--show-output", dest="show_output", action="store_true", help="display compiled script (False)")

    args = parser.parse_args()
    program = args.program
    macro_run_number = args.macro
    verbose_mode = args.verbose
    debug_mode = args.debug
    legacy_mode = args.legacy
    presets = args.presets
    dryrun = args.dryrun
    show_output = args.show_output

    starting_macro = 10
    num_macro_chars = 25
    ending_macro = 50
    number_of_sequencers = 10
    show_output = args.show_output

def initialize():
    global app_description, num_leds, starting_macro, num_macro_chars, ending_macro, number_of_sequencers, bytes_programmed
    app_description = "Apollo Lighting System - Macro Programmer v.2.0 6-1-2018"
    get_options()
    if not validate_options():
        sys.exit("\nExiting...\n")

    bytes_programmed = 0
    lc.begin(verbose_mode)

    if dryrun:
      lc.pause()
    else:
      lc.attention()
      lc.stop_all()

    num_leds = lc.get_num_leds()
    ui.begin(verbose_mode)
    starting_macro = lc.get_first_eeprom_macro()
    num_macro_chars = lc.get_num_macro_chars()
    ending_macro = starting_macro + (1024 / num_macro_chars)
    number_of_sequencers = lc.get_num_sequencers()
    all_presets = merge_two_dicts(get_device_presets(), get_command_line_presets())
    mc.begin(lc, verbose_mode, all_presets, starting_macro, ending_macro, number_of_sequencers)
    if dryrun:
      lc.resume()

# https://stackoverflow.com/questions/38987/how-to-merge-two-dictionaries-in-a-single-expression
def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z

def get_command_line_presets():
    result = {}
    for preset in presets:
      args = preset.split("=")
      result[args[0]] = args[1]
    return result

def get_device_presets():
    return {
      "NUM-LEDS": num_leds
    }

# returns True if they're valid
def validate_options():
    errors = False
    return not errors

def set_macro(macro_num, macro_text, expected_bytes):
    global macro_count, bytes_programmed

    bytes = 0
    try:
        bytes = lc.set_macro(macro_num, macro_text, expected_bytes, debug_mode)
        bytes_programmed += bytes

    except StandardError, e:
      print str(e) + " - retrying"
      try:
        lc.set_macro(macro_num, macro_text, expected_bytes, debug_mode)        
      except StandardError, e:
        sys.exit("\nUnable to program macros. Macro file may be corrupt.")

    lc.command_str(str(bytes/2) + ":pal:flu")
    macro_count += 1

    if not debug_mode:                                             
        ui.write(tc.green('.'))

def set_script(script_text):
    global macro_count, bytes_programmed
    try:
        bytes = lc.command_int(script_text);
        bytes_programmed += bytes

        ui.report_verbose("bytes programmed: " + str(bytes))

        lc.command_str(str(bytes/2) + ":pal:flu")
        macro_count += 1

        if not debug_mode:
            ui.write(tc.green('.'))

    except StandardError, e:
      print str(e) + " - retrying"
      set_script(script_text)

def import_file(program_name):
    script = []
    show_comments = True
    program_name = "./" + program_name

    if not program_name.endswith(".mac"):
        program_name = program_name  + ".mac"

    file = open(program_name, "r")
    for line in file:
        line = line.strip()
        if len(line) == 0:
            continue
        if line[0] == "#":
            if show_comments:
                print tc.yellow(line[1:].strip())
            continue
        else:
            if show_comments:
                print
                show_comments = False
        script.append(line)
    return script

def program_macros(program_name):
    compiled_script = mc.compile_file(program_name)

    if verbose_mode:
        ui.report_verbose("compiled script:")
        for script_text in compiled_script:
            ui.report_verbose(script_text)

    if show_output and not verbose_mode:
        ui.report_info("compiled script:")
        for script_text in compiled_script:
            ui.report_info_alt(script_text)

    if not mc.compilation_valid(compiled_script):
      ui.report_error("Compilation failed!")
      if not verbose_mode:
        print_script(compiled_script)
      sys.exit("\nExiting...\n")

    if not dryrun:
      for script_text in compiled_script:
        set_script(script_text) 

def print_script(script_lines):
  for script_text in script_lines:
    ui.report_warn(script_text)

# --------------------------------------------------------------------------
    
def introduction():
    ui.app_description(app_description)

    ui.report_verbose("verbose mode")
    ui.report_verbose("debug_mode: " + str(debug_mode))
    ui.report_verbose("legacy_mode: " + str(legacy_mode))
    ui.report_verbose()

    ui.report_info(ui.intro_entry("Number of LEDs", num_leds))
    ui.report_info(ui.intro_entry("Number of macros", (ending_macro - starting_macro) + 1))
    ui.report_info(ui.intro_entry("Number of sequencers", number_of_sequencers))
    ui.report_info(ui.intro_entry("Bytes per macro", num_macro_chars))
    ui.report_info(ui.intro_entry("First macro", starting_macro))
    ui.report_info(ui.intro_entry("Last macro", ending_macro))
    ui.report_info("program: " + tc.green(program))
    print
   
    if dryrun:
      ui.report_warn("Dry-run enabled. The device will not be programmed.")
      print

def summary():
  total_macros = (ending_macro - starting_macro) + 1
  used_macros = macro_count
  remaining_macros = total_macros - macro_count
  used_macros_percent = (100.0 * used_macros / total_macros)
  remaining_macros_percent = (100.0 * remaining_macros / total_macros)
  remaining_sequencers = mc.remaining_sequencers()
  used_sequencers = number_of_sequencers - remaining_sequencers
  remaining_sequencers_percent = round((100.0 * remaining_sequencers / number_of_sequencers))
  used_sequencers_percent = round((100.0 * used_sequencers / number_of_sequencers))
  total_macro_bytes = 1024
  remaining_macro_bytes = total_macro_bytes - bytes_programmed
  used_bytes_percent = round((100.0 * bytes_programmed / total_macro_bytes))
  remaining_bytes_percent = round((100.0 * remaining_macro_bytes / total_macro_bytes))
  print
  print tc.green("%d Macros successfully programmed" % macro_count)
  print tc.yellow("%d Macros remaining (%d%%)" % (remaining_macros, remaining_macros_percent))
  print tc.yellow("%d Used macro bytes (%d%%)" % (bytes_programmed, used_bytes_percent))
  print tc.yellow("%d macro bytes remaining (%d%%)" % (remaining_macro_bytes, remaining_bytes_percent))
  print tc.yellow("%d Used sequencers (%d%%)" % (used_sequencers, used_sequencers_percent))
  print tc.yellow("%d free sequencers remaining (%d%%)" % (remaining_sequencers, remaining_sequencers_percent))
  print

def upload_programs():
    program_macros(program)

def run_default_macro():
    if dryrun:
        pass
    else:
        resolved = mc.get_resolved()
        if "%run-macro" in resolved:
          lc.run_macro(resolved["%run-macro"])
        else:
          lc.run_macro(macro_run_number)

############################################################################

def setup():
    initialize()
    introduction()

def loop():
    upload_programs()
    run_default_macro()
    summary()
    sys.exit()

if __name__ == '__main__':
    setup()
    while True:
#        try:
       loop()
#        except KeyboardInterrupt:
#            sys.exit("\nExiting...\n")
#        except Exception:
#            raise

