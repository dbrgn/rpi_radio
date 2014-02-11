Raspi Radio
===========

This repository consists of different parts: The webinterface and the
controller.

Controller
----------

- ``main.py``: This is the file that's used to start the controller. It
  controls the screen and does event dispatching.
- ``buttons.py``: Some constants that are used to identify button pushes.
- ``events.py``: Everything related to the event system. It contains a
  synchronized FIFO event queue and the event loop.
- ``dispatchers.py``: Dispatchers are used to handle specific events, for
  example a button press or a refresh event. Dispatcher instances can be
  attached to the dispatcher manager with a selector function. If the selector
  function returns ``True``, the dispatcher is called.
- ``messages.py``: The message types that can be sent to the event loop.
- ``screen.py``: The virtual screens that are printed to the LCD.
- ``input_worker.py``: A worker thread that listens for user input via keyboard.
  This is only used for debugging purposes.

To start the controller from the command line::

    python -m controller.main

Web
---

The web interface is used to configure the player, and things like WLAN.

It uses Flask as a web microframework.

To start the webserver from the command line::

    cd web
    python server.py
