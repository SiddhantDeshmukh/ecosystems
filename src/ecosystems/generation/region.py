from typing import Dict, List


class Region:
    def __init__(self, name: str, region_type: str,
                 affinities: List[str]) -> None:
        self.name = name
        self.type = region_type
        self.affinities = list(set(affinities))  # ensure unique

    @classmethod
    def from_region(cls, region, name="", region_type="", affinities=[]):
        # Copy properties from 'region', overwrite with kwargs
        if not name:
            name = region.name
        if not region_type:
            region_type = region.type
        if not affinities:
            affinities = region.affinities

        return cls(name, region_type, affinities)

    def __str__(self) -> str:
        return self.name


def add_region_affinities(*regions) -> List[str]:
    # Combine regions' affinities, returning a unique list
    affinities = []
    for reg in regions:
        affinities.extend(reg.affinities)
    return list(set(affinities))


def get_region_affinities(region_affinities: Dict,
                          region_type: str) -> List[str]:
    # Search through the dictionary of region affinities to find where
    # a name is 'region_type', return the corresponding affinities
    for region in region_affinities["region"]:
        if region["name"] == region_type:
            return region["affinities"]

    print(f"\'{region}\' not found in list.")
    return []
