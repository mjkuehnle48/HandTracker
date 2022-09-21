# HandTracker
# WINDOWS ONLY

# Uses mediapipe to capture hand in each frame and then uses hand coordinates to perform relative calculations based on hand/finger position to control mouse.

# The tip of the middle finger controls the mouse cursor, the responsiveness of the cursor is a function of the hand's distance from the screen so as to implement more rigid cursor control when the hand is further away and less certain to the code.



#BASIC CURSOR CONTROLS
-INDEX FINGER DOWN THEN UP (LEFT CLICK)
-RING FINGER DOWN THEN UP (RIGHT CLICK)
-THUMB IN TOWARD PALM (SCROLL UP)
-PINKY DOWN (SCROLL DOWN)

#ADVANCED CONTROLS
-MOVE HAND CLOSE TO FRONT OF CAMERA (OPENS WINDOWS DICTATION)
-BRING TIP OF THUMB AND TIP OF PINKY TOGETHER (OPENS TASK VIEW)

# Contributing

After cloning the repository, install dependencies in a fresh virtual environment:

```console
cd path/to/the/repo
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
pip install -r requirements_dev.txt
```

[requirements.txt](requirements.txt) lists the dependencies used by the application.

[requirements_dev.txt](requirements_dev.txt) lists the libraries used to facilitate development, including formatter, linter, and import sorter.

If your editor is not configured to automatically run style checks, you can use the [check_style.py](check_style.py) script to validate the code's style before committing:

```console
python check_style.py
```

Or invoke it from a pre-commit hook - instructions in the docstring. Bypassing the checks (not recommended):

```console
git commit -m "Your commit message" --no-verify
```

<!-- Note from Vincent: I'm a coder that's pretty new to open source, so do let me know if the changes I made can be improved. I always try to strive for "best practices". -->
