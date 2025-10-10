import dearpygui.dearpygui as dpg
from .shared import sort_callback


def make_table(stats_df, parent):
    with dpg.table(
        resizable=True,
        sortable=True,
        callback=lambda sender, stat_specs: sort_callback(stats_df, sender, stat_specs),
        parent=parent,
    ) as table:
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

    return table


def init(reader, parent):
    with dpg.child_window(
        tag="Songs_window",
        parent=parent,
    ) as window:
        all_df = reader.process("spotify_track_uri")
        curr_year = "All_songs"

        def change_year(year):
            nonlocal table, curr_year

            dpg.bind_item_font(curr_year, "default_font")
            dpg.bind_item_font(str(year) + "_songs", "bold_font")
            curr_year = str(year) + "_songs"

            dpg.delete_item(table)

            if year == "All":
                table = make_table(all_df, window)
            else:
                df = reader.by_year_and_process(year, "spotify_track_uri")
                df["ts"] = all_df["ts"]
                table = make_table(df, window)

        with dpg.group(horizontal=True):
            years = sorted(all_df["ts"].dt.year.unique().tolist(), reverse=True)

            dpg.add_button(
                label="All",
                tag="All_songs",
                callback=lambda: change_year("All"),
            )
            dpg.bind_item_font("All_songs", "bold_font")

            for year in years:
                dpg.add_button(
                    label=str(year),
                    tag=str(year) + "_songs",
                    callback=(lambda x: (lambda: change_year(x)))(year),
                )

        table = make_table(all_df, window)
