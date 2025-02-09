import json
import requests
from typing import Any, Optional
from dataclasses import dataclass


@dataclass
class ChimuSearchDict:
    # 1 ranked, 2 approved, 3 qualified, 4 loved, 0 pending, -1 wip, -2 graveyard
    status: Optional[int] = None
    # 0 standard, 1 taiko, 2 CtB, 3 mania
    mode: Optional[int] = None
    # 2 game, 3 anime, 4 rock, 5 pop, 6 other, 7 novelty, 9 hiphop, 10 electronic
    genre: Optional[int] = None
    # 2 english, 3 japanese, 4 chinese, 5 instrument, 6 korean, 7 french, 8 german, 9 swedish, 10 spanish, 11 italian
    language: Optional[int] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    min_bpm: Optional[int] = None
    max_bpm: Optional[int] = None
    min_ar: Optional[float] = None
    max_ar: Optional[float] = None
    min_diff: Optional[float] = None
    max_diff: Optional[float] = None
    min_hp: Optional[float] = None
    max_hp: Optional[float] = None
    min_cs: Optional[float] = None
    max_cs: Optional[float] = None
    min_od: Optional[float] = None
    max_od: Optional[float] = None

    def get_dict(self) -> dict[str, Any]:
        _dict = {}
        for key in self.__dict__:
            if self.__dict__[key] != None:
                _dict[key] = self.__dict__[key]
        return _dict


def chimu_search(
    settings: ChimuSearchDict,
    offset: tuple[int, int] = (0, 100000000),
    filename: str = "",
) -> None:
    beatmaps = []
    new_settings = settings.get_dict()
    print(new_settings)
    max_retry = 10
    retry = 0

    while True:
        print(f"OFFSET {offset[0]}/{offset[1]}")

        try:
            response = requests.get(
                "https://api.chimu.moe/v1/search",
                params={**new_settings, "offset": offset[0]},
            )
        except:
            print(f"request error {offset[0]}")
            continue

        if not response.ok:
            print(f"bad response {offset[0]}")
            if retry >= max_retry:
                return
            retry += 1
            continue

        try:
            json_response = json.loads(response.text)
        except json.JSONDecodeError:
            print(f"json loads error! {offset[0]}")
            continue

        if not json_response.get("data"):
            print(json_response)
            print(f"No Data Found on Offset {offset}")
            return

        if type(json_response.get("data")) == list:
            beatmaps += json_response.get("data")
            offset = (offset[0] + len(json_response.get("data")), offset[1])

            with open(filename, "w") as f:
                f.write(json.dumps(beatmaps))

            retry = 0

            if offset[0] >= offset[1]:
                print(f"Finished. Total {len(beatmaps)}")
                return
        else:
            print("request response is invalid or not a list")


def chimu_beatmapset_parser(beatmapsets: list[Any]) -> list[Any]:
    beatmaps = []

    for beatmapset in beatmapsets:
        for difficulty in beatmapset.get("ChildrenBeatmaps"):
            beatmaps.append(
                {
                    "title": beatmapset.get("Title"),
                    "difficulty_name": difficulty.get("DiffName"),
                    "beatmap_status": beatmapset.get("RankedStatus"),
                    "beatmapset": beatmapset.get("SetId"),
                    "beatmap_id": difficulty.get("BeatmapId"),
                    "gamemode": difficulty.get("Mode"),
                    "difficulty_ar": difficulty.get("AR"),
                    "difficulty_hp": difficulty.get("HP"),
                    "bpm": difficulty.get("BPM"),
                    "play_length": difficulty.get("TotalLength"),
                    "difficulty_od": difficulty.get("OD"),
                    "favorites": beatmapset.get("Favourites"),
                    "difficulty": difficulty.get("DifficultyRating"),
                    "difficulty_cs": difficulty.get("CS"),
                    "pass_count": difficulty.get("Passcount"),
                    "language": beatmapset.get("Language"),
                    "genre": beatmapset.get("Genre"),
                    "total_length": difficulty.get("TotalLength"),
                    "play_count": difficulty.get("Playcount"),
                    "artist": beatmapset.get("Artist"),
                    "creator": beatmapset.get("Creator"),
                }
            )

    return beatmaps


def chimu_test() -> None:
    settings = ChimuSearchDict(status=1)
    chimu_search(
        settings=settings, filename="all-ranked-06-25-23.json", offset=(0, 10000)
    )


if __name__ == "__main__":
    chimu_test()
