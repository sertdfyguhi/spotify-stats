import dearpygui.dearpygui as dpg
from .shared import sort_callback
import pandas as pd


def init(reader, parent):
    with dpg.child_window(
        tag="Months_window",
        parent=parent,
    ):
        stats_df = reader.process(
            pd.Grouper(key="ts", freq="ME"),
            agg_funcs={
                "master_metadata_track_name": pd.Series.mode,
                "master_metadata_album_artist_name": pd.Series.mode,
                "master_metadata_album_album_name": pd.Series.mode,
            },
        )
        stats_df.reset_index(drop=True, inplace=True)
        stats_df.dropna(inplace=True)

        with dpg.table(
            resizable=True,
            sortable=True,
            callback=lambda sender, stat_specs: sort_callback(
                stats_df, sender, stat_specs
            ),
        ):
            dpg.add_table_column(label="Month", user_data="ts")
            dpg.add_table_column(label="Top Song", no_sort=True)
            dpg.add_table_column(label="Top Album", no_sort=True)
            dpg.add_table_column(label="Top Artist", no_sort=True)
            dpg.add_table_column(
                label="Minutes", user_data="ms_played", prefer_sort_descending=True
            )

            row_ids = []

            for i, row in stats_df.iterrows():
                with dpg.table_row() as row_id:
                    dpg.add_text(row["ts"].strftime("%Y-%m"))

                    for val in [
                        row["master_metadata_track_name"],
                        row["master_metadata_album_album_name"],
                        row["master_metadata_album_artist_name"],
                    ]:
                        dpg.add_text(
                            val if type(val) == str else ", ".join(val.tolist())
                        )

                    dpg.add_text(f"{row["ms_played"] / 60000:.1f}")

                row_ids.append(row_id)

            stats_df["id"] = row_ids
