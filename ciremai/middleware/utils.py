
def is_float(str):
    try:
      fl = float(str)
      return True
    except ValueError:
      return False