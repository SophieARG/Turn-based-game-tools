# Turn-based-game-tools

## How can I use `ExceptionManager.py`

**It's necessary to use `object.__new__` to setup an instance of your player.**

```python
player = Player('player', object.__new__(Module))  # Module is your player
player.call("__init__")  # initialize
player.call("method")  # call the method of player
```
