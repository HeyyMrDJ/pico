from phew import server, connect_to_wifi
from phew.template import render_template
from machine import Pin
import secrets

connect_to_wifi(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)

led = Pin("LED", Pin.OUT)

# basic response with status code and content type
@server.route("/basic", methods=["GET", "POST"])
def basic(request):
  return "Basic Request", 200, "text/html"

# query string example
@server.route("/random", methods=["GET"])
def random_number(request):
  import random
  min = int(request.query.get("min", 0))
  max = int(request.query.get("max", 100))
  return str(random.randint(min, max))

# catchall example
@server.catchall()
def catchall(request):
  return "Page not found", 404

@server.route("/test")
def index(request):
    return render_template("template.html", name="Engineering Night", title="Engineering night site", content="This content has been injected")

@server.route("/led_on")
def led_on(request):
    led.on()
    return "LED turning on", 200

@server.route("/led_off")
def led_off(request):
    led.off()
    return "LED turning off", 200
    
@server.route("/")
def main_route(request):
    return render_template("template.html", name="Engineering Night", title="Engineering night site", content="This content has been injected")

# start the webserver
server.run()
