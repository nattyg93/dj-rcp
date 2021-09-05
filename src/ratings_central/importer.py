"""Import user ratings from ratings central lists."""
import csv
import zipfile
from io import BytesIO, StringIO
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

import requests
from django.db.models import Model
from django.utils.dateparse import parse_date

from ratings_central import models


def strip_whitespace(to_strip: str) -> str:
    r"""Strip whitespace including \ufeff."""
    bad_chars = "\ufeff"
    return to_strip.strip().strip(bad_chars)


def download_rc_lists(director: models.Director) -> Dict[str, str]:
    """Download and unzip the ratings central zipped lists."""
    response = requests.post(
        "https://www.ratingscentral.com/ZippedListDownload.php?Version=5",
        data={"LoginID": director.rc_id, "LoginPassword": director.password},
    )
    with zipfile.ZipFile(BytesIO(response.content)) as zipped_download_list:
        return {
            name: strip_whitespace(zipped_download_list.read(name).decode("utf-8"))
            for name in zipped_download_list.namelist()
        }


def import_zipped_list(director: models.Director) -> None:
    """Download and import the zipped list."""
    data = download_rc_lists(director)
    club_list_name = "ClubList.csv"
    player_list_name = "RatingList.csv"
    if club_list_name in data:
        import_club_list(data[club_list_name])
    if player_list_name in data:
        import_player_list(data[player_list_name])


def import_club_list(club_list: str) -> None:
    """Import the list of clubs."""
    import_data_to_model(
        model=models.Club,
        id_mapping=("ID", "rc_id"),
        defaults_mapping={
            "Name": "name",
            "Nickname": "nickname",
            "Address1": "address_one",
            "Address2": "address_two",
            "City": "city",
            "State": "na_state",
            "Province": "world_province",
            "PostalCode": "postal_code",
            "Country": "country",
            "Email": "email",
            "Website": "website",
            "Phone": "phone",
            "Sport": "sport",
            "Status": "status",
        },
        data=club_list,
    )


def import_player_list(player_list: str) -> None:
    """Import the list of players."""
    import_data_to_model(
        model=models.Player,
        id_mapping=("ID", "rc_id"),
        defaults_mapping={
            "Name": "name",
            "Rating": "rating",
            "StDev": "st_dev",
            "LastPlayed": ("last_played", parse_date),
            "Club": "rc_primary_club_id",
            "Address1": "address_one",
            "Address2": "address_two",
            "City": "city",
            "State": "na_state",
            "Province": "world_province",
            "PostalCode": "postal_code",
            "Country": "country",
            "Email": "email",
            "Birth": ("birth", parse_date),
            "Sex": "gender",
            "Sport": "sport",
            "USATT": "usatt_id",
            "TTA": "tta_id",
            "ITTF": "ittf_id",
            "Deceased": ("deceased", lambda v: v == "D"),
        },
        data=player_list,
    )


def import_data_to_model(
    model: Type[Model],
    id_mapping: Tuple[str, str],
    defaults_mapping: Dict[str, Union[str, Tuple[str, Callable[[str], Any]]]],
    data: str,
):
    """Import the csv data to a model."""
    id_key, model_rc_id = id_mapping
    instances: Dict[str, Model] = {}
    fields = [
        field[0] if isinstance(field, tuple) else field
        for field in defaults_mapping.values()
    ]
    for row in csv.DictReader(StringIO(data)):
        if id_key not in row:
            continue
        mapped_values = {model_rc_id: row[id_key]}
        for key, value in row.items():
            if key not in defaults_mapping:
                continue
            mapped_key = defaults_mapping[key]
            converter: Optional[Callable[[str], Any]] = None
            if isinstance(mapped_key, tuple):
                converter = mapped_key[1]  # type: ignore
                mapped_key = mapped_key[0]
            mapped_values[mapped_key] = value if converter is None else converter(value)
        instances[row[id_key]] = model(**mapped_values)
        if len(instances) >= 1000:
            bulk_update_or_create(model, instances, model_rc_id, fields)
            instances = {}
    if instances:
        bulk_update_or_create(model, instances, model_rc_id, fields)


def bulk_update_or_create(
    model: Type[Model],
    instances: Dict[str, Model],
    model_rc_id: str,
    fields: List[str],
):
    """Bulk update or create the instances."""
    to_create = {**instances}
    to_update = []
    for primary_key, id_value in model.objects.filter(
        **{f"{model_rc_id}__in": instances.keys()}
    ).values_list("pk", model_rc_id):
        instance = to_create.pop(str(id_value), None)
        if instance is None:
            continue
        instance.pk = primary_key
        to_update.append(instance)
    model.objects.bulk_create(to_create.values())
    model.objects.bulk_update(to_update, fields=fields)
