"""An API and CLI for reporting CoCoRaHS observations."""

from configparser import RawConfigParser
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

import click
import requests

__version__ = "0.1.2"


class CoCoRaHS:
    root_url = "https://api2.cocorahs.org/api/"

    def __init__(self, username: str, password: str):
        self.auth = (username, password)

    def request(self, method: str, url: str, **kwargs):
        kwargs.setdefault("auth", self.auth)
        return requests.request(method, urljoin(self.root_url, url), **kwargs)

    def get_identity(self):
        return self.request("GET", "identity").json()

    def new_report(
        self,
        station: str,
        percipitation: float,
        trace: bool,
        observation_time: datetime = datetime.now(),
    ):
        return self.request(
            "POST",
            "DailyPrecipObs",
            data=dict(
                obsDateTime=observation_time.strftime("%Y-%m-%dT%H:%M:%S"),
                stationNumber=station,
                entryDateTime=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                source="PyCoCoraHS (https://github.com/dschep/PyCoCoraHS/)",
                units="english",
                gaugeCatch=percipitation,
                gaugeCatchIsTrace=trace,
            ),
        ).json()


@click.command()
@click.option("--station", help="The CoCoRaHS station code", default=None)
@click.option("--username", help="Your CoCoRaHS username", prompt=True)
@click.option("--password", help="Your CoCoRaHS password", prompt=True, hide_input=True)
@click.argument("percipitation", type=lambda val: val if val == "T" else float(val))
def cli(station, username, password, percipitation):
    """Report PERCIPITATION amount to CoCoRaHS. Enter T for trace amounts."""
    api = CoCoRaHS(username, password)

    if station is None:
        identity = api.get_identity()
        if len(identity["stations"]) == 1:
            station = identity["stations"][0]["stationNumber"]
        else:
            station = click.prompt(
                "Station",
                type=click.Choice(
                    [station["stationNumber"] for station in identity["stations"]]
                ),
            )

    resp = api.new_report(
        station,
        percipitation="0.0" if percipitation == "T" else percipitation,
        trace=percipitation == "T",
    )

    if resp.get("status") == "error":
        print(f"error - {resp['message']}")
    else:
        print(
            f"Created new report: https://www.cocorahs.org/ViewData/ViewDailyPrecipReport.aspx?DailyPrecipReportID={resp['uid']}"
        )


def read_cli_config():
    config_file = Path(click.get_app_dir("cocorahs")) / "config.ini"

    if config_file.exists():
        parser = RawConfigParser()
        parser.read([config_file])
        return parser["CoCoRaHS"]


def main():
    cli(auto_envvar_prefix="COCORAHS", default_map=read_cli_config())


if __name__ == "__main__":
    main()
