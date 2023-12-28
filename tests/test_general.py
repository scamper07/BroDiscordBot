import pytest
from src.cogs.misc.general import General


@pytest.mark.asyncio
async def test_get_xkcd_comic():
    json_response = await General.get_xkcd_comic()
    assert type(json_response["title"]) is str and type(json_response["img"]) is str
