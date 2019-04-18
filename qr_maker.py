from __future__ import print_function
import os
import random
import string
from qrcodegen import QrCode
import cairosvg
import click

svg_wrapper = """<?xml version="1.0" encoding="UTF-8"?>
	<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
		{content}
	"""

svg_mingl_logo_template = """	
	<g transform="translate({translate_x} {translate_y})" id="MINGL_LOGO_MIDDLE">
		<g transform="scale({scale_factor})">
			<rect width="100" height="100" ry="10" rx="10" fill="#00384D" style="stroke: white; stroke-width: 5"/>
			<g clip-path="url(#clip0)" >
				<path d="M51.068 11C40.444 11 32.893 18.89 32.893 28.1C32.893 37.31 40.444 45.2 51.068 45.2C61.692 45.2 69.243 37.31 69.243 28.1C69.243 18.89 61.692 11 51.068 11ZM51.068 38.205C49.7186 38.2405 48.3757 38.0054 47.1185 37.5135C45.8614 37.0216 44.7156 36.283 43.7485 35.3411C42.7815 34.3992 42.013 33.2731 41.4882 32.0294C40.9634 30.7857 40.693 29.4494 40.693 28.0995C40.693 26.7496 40.9634 25.4133 41.4882 24.1696C42.013 22.9259 42.7815 21.7998 43.7485 20.8579C44.7156 19.916 45.8614 19.1774 47.1185 18.6855C48.3757 18.1936 49.7186 17.9585 51.068 17.994C52.4175 17.9585 53.7604 18.1936 55.0175 18.6855C56.2746 19.1774 57.4205 19.916 58.3875 20.8579C59.3545 21.7998 60.1231 22.9259 60.6478 24.1696C61.1726 25.4133 61.443 26.7496 61.443 28.0995C61.443 29.4494 61.1726 30.7857 60.6478 32.0294C60.1231 33.2731 59.3545 34.3992 58.3875 35.3411C57.4205 36.283 56.2746 37.0216 55.0175 37.5135C53.7604 38.0054 52.4175 38.2405 51.068 38.205V38.205Z" fill="white"/>
				<path d="M51.068 55.122C40.444 55.122 32.893 63.012 32.893 72.222C32.893 81.432 40.444 89.322 51.068 89.322C61.692 89.322 69.243 81.433 69.243 72.222C69.243 63.011 61.692 55.122 51.068 55.122ZM51.068 82.328C49.7201 82.3608 48.3793 82.1237 47.1245 81.6306C45.8696 81.1375 44.7261 80.3984 43.7612 79.4567C42.7963 78.515 42.0295 77.3898 41.506 76.1474C40.9824 74.9049 40.7127 73.5703 40.7127 72.222C40.7127 70.8737 40.9824 69.5391 41.506 68.2966C42.0295 67.0542 42.7963 65.929 43.7612 64.9873C44.7261 64.0456 45.8696 63.3065 47.1245 62.8134C48.3793 62.3203 49.7201 62.0832 51.068 62.116C52.4159 62.0832 53.7567 62.3203 55.0115 62.8134C56.2664 63.3065 57.4099 64.0456 58.3748 64.9873C59.3397 65.929 60.1065 67.0542 60.63 68.2966C61.1536 69.5391 61.4233 70.8737 61.4233 72.222C61.4233 73.5703 61.1536 74.9049 60.63 76.1474C60.1065 77.3898 59.3397 78.515 58.3748 79.4567C57.4099 80.3984 56.2664 81.1375 55.0115 81.6306C53.7567 82.1237 52.4159 82.3608 51.068 82.328V82.328Z" fill="white"/>
				<path d="M35.098 55.123C37.9135 55.123 40.196 52.9014 40.196 50.161C40.196 47.4206 37.9135 45.199 35.098 45.199C32.2825 45.199 30 47.4206 30 50.161C30 52.9014 32.2825 55.123 35.098 55.123Z" fill="white"/>
			</g>
			<defs>
				<clipPath id="clip0">
					<rect width="39.243" height="78.321" fill="white" transform="translate(30 11)"/>
				</clipPath>
			</defs>
		</g>	
	</g>
"""

svg_mingl_text_template = """
	<g transform="translate(40 90)" id="MINGL_LOGO_TEXT_BOTTOM">
		<g transform="scale(0.1)">
			<rect width="200" height="100" fill="white"/>
			<path d="M79.4601 64.7029V27.5732H86.4082V64.7029H79.4601Z" fill="#00384D"/>
			<path d="M54.6668 26.9766C49.3133 26.9766 44.0562 29.867 42.0456 31.9349C39.6115 28.7271 35.7855 26.8827 31.7598 26.9766C26.3603 26.9766 21.3238 29.7845 19.4808 31.6274L18.9719 27.5732H13V64.702H19.9524V38.1048C23.1659 34.8218 26.6139 33.4392 30.3007 33.4392C35.3546 33.4392 37.4894 36.5545 37.4894 40.7546V64.6994H44.4374V39.4258C44.4385 38.5663 44.3577 37.7087 44.196 36.8646C46.6798 34.6565 49.8886 33.4383 53.212 33.4418C58.318 33.4418 60.4007 36.5884 60.4007 40.7572V64.702H67.3487V39.4284C67.3505 32.2293 61.9145 26.9766 54.6668 26.9766Z" fill="#00384D"/>
			<path d="M105.78 64.7029H98.8322V27.5732H104.801L105.31 31.6266C107.153 29.7845 112.19 26.9766 117.589 26.9766C124.837 26.9766 130.273 32.2293 130.273 39.4293V64.7029H123.325V40.7581C123.325 36.3903 121.096 33.4418 116.136 33.4418C112.449 33.4418 108.999 34.8244 105.787 38.1074L105.78 64.7029Z" fill="#00384D"/>
			<path d="M156.011 26.9766C146.784 26.9766 140.226 33.8282 140.226 41.8281C140.226 49.8279 146.784 56.6796 156.011 56.6796C165.239 56.6796 171.797 49.8271 171.797 41.8281C171.797 33.8291 165.239 26.9766 156.011 26.9766ZM156.011 50.6044C151.193 50.4818 147.375 46.4979 147.456 41.6787C147.538 36.8595 151.489 33.0072 156.309 33.048C161.129 33.0888 165.014 37.0074 165.014 41.8272C164.998 44.1892 164.036 46.4463 162.345 48.0952C160.654 49.744 158.373 50.6476 156.011 50.6044Z" fill="#00384D"/>
			<path d="M156.011 65.297C146.784 65.297 140.226 72.1495 140.226 80.1485C140.226 88.1475 146.784 95 156.011 95C165.239 95 171.797 88.1475 171.797 80.1485C171.797 72.1495 165.239 65.297 156.011 65.297ZM156.011 88.9204C151.192 88.7979 147.374 84.8129 147.456 79.993C147.539 75.1732 151.492 71.3214 156.312 71.3641C161.133 71.4068 165.017 75.3279 165.014 80.1485C164.998 82.5104 164.036 84.7674 162.345 86.4161C160.654 88.0649 158.373 88.9682 156.011 88.9248V88.9204Z" fill="#00384D"/>
			<path d="M186.702 17H179.822V64.7029H186.702V17Z" fill="#00384D"/>
			<path d="M142.141 65.297C144.587 65.297 146.569 63.3675 146.569 60.9874C146.569 58.6073 144.587 56.6779 142.141 56.6779C139.696 56.6779 137.714 58.6073 137.714 60.9874C137.714 63.3675 139.696 65.297 142.141 65.297Z" fill="#00384D"/>
		</g>
	</g>
"""

svg_position_template = """	
	<g transform="translate({translate_x} {translate_y})" id="MINGL_LOGO_MIDDLE">
		<g transform="scale({scale_factor})">
			{content}
		</g>	
	</g>
"""

@click.command()
@click.option('-c', '--color', default='#00384D')
@click.option('-d', '--design', default='special', type=click.Choice(['special', 'round', 'square']))
@click.option('-e', '--eyes', default='square', type=click.Choice(['square']))
@click.option('-ec', '--eye_color', default='#00384D')
@click.option('-ft', '--file_type', default='pdf', type=click.Choice(['pdf', 'png', 'svg']))
@click.option('-fn', '--file_name', default='aaa')
@click.option('-v', '--value', prompt="Please enter a value for the qr")
@click.option('--logo/--no_logo', default=True)
@click.option('--grid/--no_grid', default=False)
def main(color, design, eyes, eye_color, file_type, file_name, value, logo, grid):
	"""The main application program."""

	if grid:
		final_svg = make_grid(color, design, eyes, eye_color, file_type, logo, grid)
	else: 
		final_svg = make_one_qr_svg(color, design, eyes, eye_color, file_type, value, logo, grid, errcorlvl=QrCode.Ecc.MEDIUM)

	if file_type == 'pdf':
		cairosvg.svg2pdf(bytestring=final_svg, write_to=file_name + ".pdf")
	if file_type == 'png':
		cairosvg.svg2png(bytestring=final_svg, write_to=file_name + ".png")
	if file_type == 'svg':
		with open(file_name + ".svg", "w") as text_file:
			print(final_svg, file=text_file)

def make_grid(color, design, eyes, eye_color, file_type, logo, grid):
	grid_svg_template = ''
	with open('magnus_grid.svg', 'r') as grid_file:
		grid_svg_template = grid_file.read()
	x_offset = 33
	x_cell_width = 110.35
	y_offset = 123
	top_white_space = 24
	white_space = 12.5
	padding = 5
	scale_factor = 0.75
	for i in range(25):
		translate_x = x_offset + white_space + padding + i * x_cell_width
		for j in range(35):
			value= 'https://mingl.no/' + ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=12))
			qr_sgv = make_one_qr_svg(color, design, eyes, eye_color, file_type, value, logo, grid, errcorlvl=QrCode.Ecc.MEDIUM)
			translate_y= y_offset + top_white_space + padding + j * (padding + white_space + padding + 78) + int(j / 5) * 137
			positioned_qr = svg_position_template.format(content=qr_sgv, translate_x=translate_x, translate_y=translate_y, scale_factor=scale_factor)
			grid_svg_template = grid_svg_template + positioned_qr

	return grid_svg_template + '\n</svg>'

def make_one_qr_svg(color, design, eyes, eye_color, type, value, logo, grid, errcorlvl, width_cm='3cm', height_cm='3cm'):
	qr = QrCode.encode_text(value, errcorlvl)
	if design == 'special':
		body = get_special(qr=qr, color=color)
	if design == 'round':
		body = get_cirles(qr=qr, color=color)
	if design == 'square':
		body = get_squares(qr=qr, color=color)
	eyes = get_squared_eyes(qr=qr, color=eye_color)
	qr_code = "\n".join([body, eyes])
	scale_factor = 80 / qr._size

	svg_wrapper_template = """
	<svg xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="0 0 100 100" stroke="none" width="{width_cm}" height="{height_cm}">
		{content}
	</svg>"""

	svg_qr_content_template = """
		<rect width="100" height="100" fill="#FFFFFF"/>
		<g transform="translate(10 10)" id="QR_BODY">
			<g transform="scale({scale_factor})">
				{qr_code}
				{mingl_logo}
			</g>
		</g>
		{mingl_text}
	"""

	mingl_text = svg_mingl_text_template
	svg_qr_code_without_logo = svg_qr_content_template.format(qr_code=qr_code, scale_factor=scale_factor, mingl_text=mingl_text, mingl_logo='{mingl_logo}')
	svg_qr_code = addLogo(svg_qr_code_without_logo, logo, qr._size)
	if not grid:
		svg_qr_code = svg_wrapper_template.format(content=svg_qr_code, width_cm=width_cm, height_cm=height_cm)
	return svg_qr_code

def addLogo(svg_qr_code_without_logo, logo, qr_size):
	svg_qr_code = ''
	logo_size = 0.2 * qr_size
	scale_factor = logo_size / 100
	translate = (qr_size / 2) - (logo_size / 2)
	corner_radius = logo_size * 0.4
	if logo:
		svg_mingl_logo = svg_mingl_logo_template.format(translate_x=translate, translate_y=translate, scale_factor=scale_factor, corner_radius=corner_radius)
		svg_qr_code = svg_qr_code_without_logo.format(mingl_logo=svg_mingl_logo)
	else :
		svg_qr_code = svg_qr_code_without_logo.format(mingl_logo='')
	return svg_qr_code

def is_part_of_eye(x, y, size):
	if (0 <= x <= 7) and ((0 <= y <= 7)):
		return True
	if (size - 7 <= x <= size) and ((0 <= y <= 7)):
		return True
	if (0 <= x <= 7) and (size - 7 <= y <= size):
		return True
	return False


def get_squares(qr, color, ):
	squares = []
	for y in range(qr._size):
		for x in range(qr._size):
			if qr.get_module(x, y) and not is_part_of_eye(x, y, qr._size):
				squares.append("<rect x='{position_x}' y='{position_y}' width='1' height='1' style='fill:{color}' />".format(position_x=x, position_y=y, color=color))
	return "\n".join(squares)

def get_cirles(qr, color, ):
	squares = []
	for y in range(qr._size):
		for x in range(qr._size):
			if qr.get_module(x, y) and not is_part_of_eye(x, y, qr._size):
				squares.append("<rect x='{position_x}' y='{position_y}' rx='1' ry='1' width='1' height='1' style='fill:{color}' />".format(position_x=x, position_y=y, color=color))
	return "\n".join(squares)

def get_special(qr, color, ):
	squares = []
	for y in range(qr._size):
		for x in range(qr._size):
			if qr.get_module(x, y) and not is_part_of_eye(x, y, qr._size):
				if (qr.get_module(x - 1, y) and qr.get_module(x + 1, y)) or (qr.get_module(x , y - 1) and qr.get_module(x, y + 1)): # two sides
					squares.append(get_square(position_x=x, position_y=y, color=color))
				else: 
					if qr.get_module(x - 1, y): # left
						if qr.get_module(x, y - 1): # top
							squares.append(get_bottom_right_round(position_x=x, position_y=y, color=color))
						if qr.get_module(x, y + 1): # bottom
							squares.append(get_top_right_round(position_x=x, position_y=y, color=color))
						if not qr.get_module(x, y - 1) and not qr.get_module(x, y + 1): # only left
							squares.append(get_right_round(position_x=x, position_y=y, color=color))
					if qr.get_module(x + 1, y): # right
						if qr.get_module(x, y - 1): # top
							squares.append(get_bottom_left_round(position_x=x, position_y=y, color=color))
						if qr.get_module(x, y + 1): # bottom
							squares.append(get_top_left_round(position_x=x, position_y=y, color=color))
						if not qr.get_module(x, y - 1) and not qr.get_module(x, y + 1): # only right
							squares.append(get_left_round(position_x=x, position_y=y, color=color))
					if qr.get_module(x, y - 1) and not qr.get_module(x - 1, y) and not qr.get_module(x + 1, y): # only top
						squares.append(get_bottom_round(position_x=x, position_y=y, color=color))
					if qr.get_module(x, y + 1) and not qr.get_module(x - 1, y) and not qr.get_module(x + 1, y): # only bottom
						squares.append(get_top_round(position_x=x, position_y=y, color=color))
					if not qr.get_module(x, y - 1) and not qr.get_module(x, y + 1) and not qr.get_module(x - 1, y) and not qr.get_module(x + 1, y): # no neighbours
						squares.append(get_circle(position_x=x, position_y=y, color=color))

	return "\n".join(squares)

def get_square(position_x, position_y, color):
	return'<path d="M{position_x} {position_y} h1 v1 h-1 z" fill="{color}" />'.format(position_x=position_x, position_y=position_y, color=color)

def get_circle(position_x, position_y, color):
	return "<rect x='{position_x}' y='{position_y}' rx='1' ry='1' width='1' height='1' style='fill:{color}' />".format(position_x=position_x, position_y=position_y, color=color)

def get_top_left_round(position_x, position_y, color):
	return'<path d="M{position_x} {position_y} v-0.5 a0.5,0.5 0 0 1 0.5,-0.5 h0.5 v1 z" fill="{color}" />'.format(position_x=position_x, position_y=position_y + 1, color=color)

def get_top_right_round(position_x, position_y, color):
	return'<path d="M{position_x} {position_y} h0.5 a0.5,0.5 0 0 1 0.5,0.5 v0.5 h-1 z" fill="{color}" />'.format(position_x=position_x, position_y=position_y, color=color)

def get_bottom_left_round(position_x, position_y, color):
	return'<path d="M{position_x} {position_y} h1 v1 h-0.5 a0.5,0.5 0 0 1 -0.5,-0.5 z" fill="{color}" />'.format(position_x=position_x, position_y=position_y, color=color)

def get_bottom_right_round(position_x, position_y, color):
	return'<path d="M{position_x} {position_y} h1 v0.5 a0.5,0.5 0 0 1 -0.5,0.5 h-0.5 z" fill="{color}" />'.format(position_x=position_x, position_y=position_y, color=color)

def get_top_round(position_x, position_y, color):
	return'<path d="M{position_x} {position_y} h-1 v-0.5 a0.5,0.5 0 0 1 1,0 z" fill="{color}" />'.format(position_x=position_x + 1, position_y=position_y + 1, color=color)

def get_bottom_round(position_x, position_y, color):
	return'<path d="M{position_x} {position_y} h1 v0.5 a0.5,0.5 0 0 1 -1,0 z" fill="{color}" />'.format(position_x=position_x, position_y=position_y, color=color)

def get_left_round(position_x, position_y, color):
	return'<path d="M{position_x} {position_y} h-0.5 a0.5,0.5 0 0 1 0,-1 h0.5 z" fill="{color}" />'.format(position_x=position_x + 1, position_y=position_y + 1, color=color)

def get_right_round(position_x, position_y, color):
	return'<path d="M{position_x} {position_y} h0.5 a0.5,0.5 0 0 1 0,1 h-0.5 z" fill="{color}" />'.format(position_x=position_x, position_y=position_y, color=color)

def get_squared_eyes(qr, color, ):
	squares = []
	for y in range(qr._size):
		for x in range(qr._size):
			if qr.get_module(x, y) and is_part_of_eye(x, y, qr._size):
				squares.append("<rect x='{position_x}' y='{position_y}' width='1' height='1' style='fill:{color}' />".format(position_x=x, position_y=y, color=color))
	return "\n".join(squares)

if __name__ == '__main__':
    main()