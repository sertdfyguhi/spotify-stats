from dateutil.tz import tzlocal
import pandas as pd
import json
import glob
import os

AGG_FUNCS = {
    "spotify_track_uri": "first",
    "master_metadata_track_name": "first",
    "master_metadata_album_artist_name": "first",
    "master_metadata_album_album_name": "first",
    "ms_played": "sum",
    "plays": "size",
    "ts": "first",
}


class ListeningHistoryReader:
    def __init__(self, folder_path):
        self.folder_path = folder_path

        json_files = glob.glob(os.path.join(folder_path, "*.json"))
        json_files.sort(key=lambda x: x[-6])

        data_list = []

        for file in json_files:
            data_list += json.load(open(file, "r"))

        self.history_df = pd.DataFrame.from_dict(data_list)
        self.history_df.drop(
            columns=[
                "platform",
                "conn_country",
                "ip_addr",
                "episode_name",
                "episode_show_name",
                "spotify_episode_uri",
                "audiobook_title",
                "audiobook_uri",
                "audiobook_chapter_uri",
                "audiobook_chapter_title",
                "reason_start",
                "reason_end",
                "shuffle",
                "skipped",
                "offline",
                "offline_timestamp",
                "incognito_mode",
            ],
            inplace=True,
        )
        self.history_df["plays"] = 1
        self.history_df["ts"] = pd.to_datetime(self.history_df["ts"])
        self.history_df["ts"] = self.history_df["ts"].dt.tz_convert(tzlocal())

    def process(self, groupby, agg_funcs={}):
        temp_dict = AGG_FUNCS.copy()
        temp_dict.update(agg_funcs)

        return self.history_df.groupby(groupby).agg(temp_dict)

    def by_year_and_process(self, year, groupby, agg_funcs={}):
        by_year_df = self.history_df.loc[self.history_df["ts"].dt.year == year]

        temp_dict = AGG_FUNCS.copy()
        temp_dict.update(agg_funcs)

        return by_year_df.groupby(groupby).agg(temp_dict)
