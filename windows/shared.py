import dearpygui.dearpygui as dpg


def sort_callback(stats_df, sender, sort_specs):
    if sort_specs is None:
        return

    sorted_df = stats_df.sort_values(
        dpg.get_item_user_data(sort_specs[0][0]),
        ascending=sort_specs[0][1] == -1,
    )
    dpg.reorder_items(sender, 1, sorted_df["id"].tolist())
