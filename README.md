# python-neon-text
Python script that generates an image with the given text, with a neon glow effect

Examples:
---------

python neon.py -t 'Happy New Year!' -f img/happy_new_year.png

![Happy new year](./img/happy_new_year.png)

python neon.py -t "This looks like Frozen" -f img/frozen_message.png --shadow 0E03D8 --fg1 00C4F0 --width 800 --height 300

![Frozen message](./img/frozen_message.png)


Dependencies:
-------------

- [PyCairo](https://cairographics.org/pycairo/)
- [Pillow](https://pillow.readthedocs.io/en/5.1.x/index.html#pillow)
