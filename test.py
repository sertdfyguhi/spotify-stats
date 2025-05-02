for column in [
    "Name",
    "Artist",
    "Album",
    "Plays",
    "Minutes",
    "First Listen",
]:
    print(f'dpg.add_table_column(label="{column}")')
