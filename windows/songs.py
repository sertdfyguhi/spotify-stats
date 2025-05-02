import dearpygui.dearpygui as dpg
from .shared import sort_callback


def init(reader, parent):
    with dpg.child_window(
        tag="Songs_window",
        parent=parent,
    ):
        stats_df = reader.process("spotify_track_uri")

        with dpg.table(
            resizable=True,
            sortable=True,
            callback=lambda sender, stat_specs: sort_callback(
                stats_df, sender, stat_specs
            ),
        ):
            dpg.add_table_column(label="Name", no_sort=True)
            dpg.add_table_column(label="Album", no_sort=True)
            dpg.add_table_column(label="Artist", no_sort=True)
            dpg.add_table_column(
                label="Plays",
                user_data="plays",
                prefer_sort_descending=True,
            )
            dpg.add_table_column(
                label="Minutes", user_data="ms_played", prefer_sort_descending=True
            )
            dpg.add_table_column(label="First Listen", user_data="ts")

            row_ids = []

            for i, row in stats_df.iterrows():
                with dpg.table_row() as row_id:
                    dpg.add_text(row["master_metadata_track_name"])
                    dpg.add_text(row["master_metadata_album_album_name"])
                    dpg.add_text(row["master_metadata_album_artist_name"])
                    dpg.add_text(row["plays"])
                    dpg.add_text(f"{row["ms_played"] / 60000:.1f}")
                    dpg.add_text(row["ts"])

                row_ids.append(row_id)

            stats_df["id"] = row_ids
