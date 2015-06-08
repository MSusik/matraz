import re

from svg_config import Config


def matraz_svg(license=None, contact=False, documentation=False, doi=None):

    blocks = re.split(r'<!-- .* -->', Config)

    image = blocks[0]
    current_box = 1

    if license:
        image += blocks[current_box]
        image += 'LICENSE (' + license + ')'
        image += blocks[current_box+1] + blocks[current_box+2]
        current_box = current_box + 3

    if contact:
        image += blocks[current_box]
        image += "CONTACT INFO"
        image += blocks[current_box+1] + blocks[current_box+2]
        current_box = current_box + 3

    if documentation:
        image += blocks[current_box]
        image += "DOCUMENTATION"
        image += blocks[current_box+1] + blocks[current_box+2]
        current_box = current_box + 3

    if doi:
        image += blocks[current_box]
        image += "DOI"
        image += blocks[current_box+1] + blocks[current_box+2]
        current_box = current_box + 3

    image += blocks[-2]
    image += blocks[-1]

    return image
