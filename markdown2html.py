#!/usr/bin/python3
"""
Script to convert Markdown to HTML.
"""
import sys
import os.path
import re
import hashlib

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: ./markdown2html.py README.md README.html',
              file=sys.stderr)
        exit(1)

    if not os.path.isfile(sys.argv[1]):
        print('Missing {}'.format(sys.argv[1]), file=sys.stderr)
        exit(1)

    with open(sys.argv[1]) as input_file:
        with open(sys.argv[2], 'w') as output_file:
            list_start, numbered_start, text_block = False, False, False
            for content in input_file:
                content = content.replace('**', '<b>', 1)
                content = content.replace('**', '</b>', 1)
                content = content.replace('__', '<em>', 1)
                content = content.replace('__', '</em>', 1)

                special_syntax = re.findall(r'\[\[.+?\]\]', content)
                inner_content = re.findall(r'\[\[(.+?)\]\]', content)
                if special_syntax:
                    content = content.replace(special_syntax[0], hashlib.md5(
                        inner_content[0].encode()).hexdigest())

                transform_syntax = re.findall(r'\(\(.+?\)\)', content)
                inner_transform = re.findall(r'\(\((.+?)\)\)', content)
                if transform_syntax:
                    transformed = ''.join(
                        char for char in inner_transform[0] if char not in 'Cc')
                    content = content.replace(transform_syntax[0], transformed)

                line_length = len(content)
                heading_content = content.lstrip('#')
                heading_level = line_length - len(heading_content)
                list_content = content.lstrip('-')
                list_marker = line_length - len(list_content)
                numbered_content = content.lstrip('*')
                numbered_marker = line_length - len(numbered_content)

                if 1 <= heading_level <= 6:
                    content = '<h{}>'.format(
                        heading_level) + heading_content.strip() + '</h{}>\n'.format(
                        heading_level)

                if list_marker:
                    if not list_start:
                        output_file.write('<ul>\n')
                        list_start = True
                    content = '<li>' + list_content.strip() + '</li>\n'
                if list_start and not list_marker:
                    output_file.write('</ul>\n')
                    list_start = False

                if numbered_marker:
                    if not numbered_start:
                        output_file.write('<ol>\n')
                        numbered_start = True
                    content = '<li>' + numbered_content.strip() + '</li>\n'
                if numbered_start and not numbered_marker:
                    output_file.write('</ol>\n')
                    numbered_start = False

                if not (heading_level or list_start or numbered_start):
                    if not text_block and line_length > 1:
                        output_file.write('<p>\n')
                        text_block = True
                    elif line_length > 1:
                        output_file.write('<br/>\n')
                    elif text_block:
                        output_file.write('</p>\n')
                        text_block = False

                if line_length > 1:
                    output_file.write(content)

            if list_start:
                output_file.write('</ul>\n')
            if numbered_start:
                output_file.write('</ol>\n')
            if text_block:
                output_file.write('</p>\n')
    exit(0)
