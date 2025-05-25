from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin, config, Undefined
from aiohttp import ClientSession
from django.conf import settings


@dataclass
class OpacScenario(DataClassJsonMixin):
    dataclass_json_config = config(undefined=Undefined.EXCLUDE)["dataclasses_json"]
    prefix: str
    description: str | None = None


async def opac_scenarios(client: ClientSession, database: str) -> list[OpacScenario]:
    r = await client.get(f"{settings.OPAC_HOSTNAME}/api/scenarios/{database}")
    r.raise_for_status()

    return OpacScenario.schema().load(await r.json(), many=True)
