#!/usr/bin/env python3

import sys, getopt
from os.path import expanduser
from file.replace import replace

help_message = """
usage: zshPlugin [-a plugin_name] [-h]

The command to add plugin in ~/.zshrc conf file

optional arguments:
-h, --help                show help message for user
-a, --add plugin_name	  add plugin in zsh conf file
-r, --remove plugin_name  remove plugin in zsh conf file
"""
operation = ''

# Command name will be zshPlugin
def usage(complete_type = 0):
	if complete_type == 1:
		print ('Error: Wrong usage for this command.')
	print (help_message)
	sys.exit()

def main(argv):
	# Find path to .vimrc file
	home_path = expanduser("~")
	zshrc_path = home_path + "/.zshrc"
	zshrc_file = open(zshrc_path)

	adding_message = 'Adding plugin {!s} in zsh now.'
	removing_message = 'Removing plugin {!s} in zsh now.'
	duplicate_message = 'The plugin {!s} already exists in zshrc now.'
	not_exist_message = 'The plugin {!s} doesn\' exist in plugins.'
	success_message = 'Successfully {!s} plugin in zshrc config file.\nPlease use :PluginInstall to install our new plugin in vim'

	# Parsing args
	try:
		opts, args = getopt.getopt(argv, "ha:r:", ["help", "add", "remove"])
	except getopt.GetoptError:
		usage(1)
	if len(opts) == 0:
		usage()
	for opt, arg in opts:
		if opt in ('-h', '--help'):
			usage()
		elif opt in ('-a', '--add'):
			operation = 'add'
			plugin_name = arg
			print (adding_message.format(plugin_name))
			for line in zshrc_file:
				if line.startswith('plugins'):
					if plugin_name in line:
						print (duplicate_message.format(plugin_name))
						sys.exit()
					line_length = len(line)
					new_line = line[: line_length - 2] + '{!s} '.format(plugin_name) + line[line_length - 2 :]
					replace(zshrc_path, line, new_line)
		elif opt in ('-r', '--remove'):
			operation = 'remove'
			plugin_name = arg
			print (removing_message.format(plugin_name))
			for line in zshrc_file:
				if line.startswith('plugins'):
					if plugin_name not in line:
						print (not_exist_message.format(plugin_name))
						sys.exit()
					plugin_index = line.find(plugin_name)
					if not line[plugin_index - 1].isspace() or not line[plugin_index + len(plugin_name)].isspace():
						print (not_exist_message.format(plugin_name))
						sys.exit()
					new_line = line[: plugin_index] + line[plugin_index + len(plugin_name) + 1 :]
					replace(zshrc_path, line, new_line)

	print (success_message.format(operation))

if __name__ == "__main__":
	main(sys.argv[1:])
