#!/usr/bin/env python3

import argparse
import glob
import os.path
import subprocess
import tempfile


def expand_template(input_file, output_file, substitution_dict):
  for old_line in input_file.readlines():
    new_line = old_line
    for old, new in substitution_dict.items():
      new_line = new_line.replace(old, new)

    output_file.write(new_line)


def main():
  parser = argparse.ArgumentParser(description='Configure and start GTKwave.')
  parser.add_argument('--tcl_template',
                      default=os.path.join(os.path.dirname(__file__), 'gtkwave.tcl.template'),
                      help='Template Tcl file for GTKwave configuration.')
  parser.add_argument('--open_level', type=int, default=2,
                      help='Hierarchy level to display by default.')
  parser.add_argument('--vcd_dir', help='Search directory for VCD files.')
  parser.add_argument('traces', nargs='*', help='Trace names to display. Globs are allowed.' +
                      ' ".vcd" extension will be added if no extension is provided.')

  args = parser.parse_args()

  if not args.traces:
    args.traces = ['*']

  vcd_files = []
  for trace in args.traces:
    base, ext = os.path.splitext(trace)
    if not ext:
      ext = '.vcd'

    path = os.path.join(args.vcd_dir, base + ext) if args.vcd_dir else base + ext
    vcd_files.extend(glob.glob(path))

  if not vcd_files:
    print('No traces {:s}match {}.'.format(
        'in {:s} '.format(args.vcd_dir) if args.vcd_dir else '',
        args.traces))
    return

  load_files = '\n'.join(['gtkwave::loadFile "{:s}"'.format(f) for f in vcd_files])

  with tempfile.TemporaryDirectory() as directory:
    tcl_name = os.path.join(directory, 'gtkwave.tcl')
    with open(args.tcl_template, 'r') as in_template, open(tcl_name, 'w') as out_template:
      expand_template(in_template, out_template,
          {'@LOAD_FILES@': load_files, '@OPEN_LEVEL@': str(args.open_level)})

    gtkwave_args = [
        'gtkwave',
        '-S',
        tcl_name,
        '--rcvar',
        'initial_window_x 2000',
        '--rcvar',
        'initial_window_y 1200',
    ]

    try:
      subprocess.run(gtkwave_args)
    except KeyboardInterrupt:
      pass


if __name__ == '__main__':
  main()
