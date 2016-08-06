#!/usr/bin/env python3

import sys, getopt
from os import listdir
from os.path import exists, expanduser
from file.replace import replace

help_message = """
usage: zshPlugin [-a/--add plugin_name] [-h/--help] [-l/--list] [-r/--remove plugin_name]

The command to add plugin in ~/.zshrc conf file

optional arguments:
-h, --help                show help message for user
-a, --add plugin_name	  add plugin in zsh conf file
-r, --remove plugin_name  remove plugin in zsh conf file
-l, --list                list all plugins in oh-my-zsh plugins directory
"""
operation = ''

adding_message = 'Adding plugin {!s} in zsh now.'
removing_message = 'Removing plugin {!s} in zsh now.'
duplicate_message = 'The plugin {!s} already exists in zshrc now.'
not_exist_message = 'The plugin {!s} doesn\' exist in plugins.'
success_message = 'Successfully {!s} plugin in zshrc config file.\nPlease source our lastest zsh configuration into terminal'

# Command name will be zshPlugin
def usage(complete_type = 0):
	if complete_type == 1:
		print ('Error: Wrong usage for this command.')
	print(help_message)
	sys.exit()

def list_plugin(zsh_plugin_path):
	print('All plugins are listed as following:')
	print(listdir(zsh_plugin_path))
	sys.exit()

def check_file(file_path, file_name):
	if not exists(file_path + file_name):
		print(not_exist_message.format(file_name))
		sys.exit()

def add_plugin(zshrc_path, plugin_name):
	for line in open(zshrc_path):
		if line.startswith('plugins'):
			if plugin_name in line:
				print (duplicate_message.format(plugin_name))
				sys.exit()
			line_length = len(line)
			new_line = line[: line_length - 2] + '{!s} '.format(plugin_name) + line[line_length - 2 :]
			replace(zshrc_path, line, new_line)

def remove_plugin(zshrc_path, plugin_name):
	for line in open(zshrc_path):
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

def main(argv):
	# Find path to .vimrc file
	home_path = expanduser("~")
	zshrc_path = home_path + "/.zshrc"
	zshrc_file = open(zshrc_path)
	zsh_plugin_path = home_path + '/.oh-my-zsh/plugins/'

	# Parsing args
	try:
		opts, args = getopt.getopt(argv, "ha:r:l", ["help", "add", "remove", "list"])
	except getopt.GetoptError:
		usage(1)
	if len(opts) == 0:
		usage()
	for opt, arg in opts:
		if opt in ('-h', '--help'):
			usage()

		elif opt in ('-l', '--list'):
			list_plugin(zsh_plugin_path)

		elif opt in ('-a', '--add'):
			operation = 'add'
			plugin_name = arg
			print (adding_message.format(plugin_name))
			check_file(zsh_plugin_path, plugin_name)
			add_plugin(zshrc_path, plugin_name)

		elif opt in ('-r', '--remove'):
			operation = 'remove'
			plugin_name = arg
			print (removing_message.format(plugin_name))
			remove_plugin(zshrc_path, plugin_name)

	print (success_message.format(operation))

if __name__ == "__main__":
	main(sys.argv[1:])
