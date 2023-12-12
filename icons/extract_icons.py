from PIL import Image

image = Image.open("weather_icons.png")

x0 = 5
y0 = 3
dx = 156
dy = dx

# PIL works from top left corner.
names = [
    ["clouds2", "clouds0", "clouds1", "pp_liquid2", "pp_liquid3"],
    ["pp_snow3", "pp_hail", "storm1", "storm2", "rainstorm"],
    ["lightning1", "lightning2", "rain", "clouds0_night", "clouds1_night"],
    ["pp_liquid1", "pp_liquid1_night", "degree", "fahrenheit", "pp_mixed"],
    ["hail_night", "thermometers", "clouds3", "umbrella", "droplet"]
]


n = 5
for i in range(n):
    x = x0 + i*dx
    for j in range(n):
        y = y0 + j*dy
        box = (x, y, x + dx, y + dy)
        sub = image.crop(box)

        name = "{}.png".format(names[j][i])
        sub.save(name, "PNG")
