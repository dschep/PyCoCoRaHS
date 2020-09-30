# PyCoCoraHS

PyCoCoraHS is a Python package providing a CLI utility and an API for uploading observations to
[CoCoRaHS](https://cocorahs.org).

## Installing
Install this package using `pip`:
```shell
python3 -m pip install --user PyCoCoraHS
```

## Using the CLI
You can invoke the CLI via `cocorahs`. Here is the help output:
```
Usage: cocorahs [OPTIONS] PERCIPITATION

  Report PERCIPITATION amount to CoCoRaHS. Enter T for trace amounts.

Options:
  --station TEXT   The CoCoRaHS station code
  --username TEXT  Your CoCoRaHS username
  --password TEXT  Your CoCoRaHS password
  --help           Show this message and exit.
```

### Configuring the CLI via a config file.
Create a file at `~/.config/cocorahs/config.ini` containing a config like the following but
changing the details to your username, password, & station.
```ini
[CoCoRaHS]
username = DanielSchep
password = hunter2
station = VA-RCC-15
```

## API Usage
Here is a simple example of making a new report via the API:
```python
from cocorahs import CoCoRaHS

api = CoCoRaHS(username='DanielSchep', password='hunter2')
api.new_report(station='VA-RCC-15', percipitation='0.1', trace=False)
```

The `new_report` function also accepts an `observation_time` keyword argument. It should be a
`datetime.datetime` object.
