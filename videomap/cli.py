# -*- coding: utf-8 -*-

"""Console script for videomap."""
import re
import sys
import pathlib

import click
import pandas as pd
import ffmpeg


frame_pattern = re.compile(
    r'(?P<frame>\d+)/(?P<zoom>\d+)/(?P<column>\d+)/(?P<row>\d+)\.(png|jpg)$'
)

@click.group()
def cli():
    pass

@cli.command()
@click.argument('frames_dir', type=click.Path(exists=True))
@click.argument('result_dir', type=click.Path(exists=False), default='result')
def convert(frames_dir, result_dir):
    """Console script for videomap."""
    frames_path = pathlib.Path(frames_dir)
    result_path = pathlib.Path(result_dir)

    tile_paths = list(frames_path.glob('**/*.png'))
    rows = []
    for tile in tile_paths:
        match = frame_pattern.search(tile.as_posix())
        match_dict = match.groupdict()
        row = {
            "match": match,
            "tile": tile,
            "column": int(match_dict["column"]),
            "frame": int(match_dict["frame"]),
            "row": int(match_dict["row"]),
            "zoom": int(match_dict["zoom"])
        }
        rows.append(row)

    # Overview of tiles
    tiles_df = pd.DataFrame(rows).infer_objects()
    tiles_df.head()

    # Convert all images per frame
    for (zoom, column, row), frames in tiles_df.groupby(['zoom', 'column', 'row']):
        # define the path of the  videos
        video_path = (result_path / str(zoom) / str(column) / str(row)).with_suffix('.mp4')

        # create an input string that reflects all images per tile
        input_path = (frames_path / '%d' / str(zoom) / str(column) / str(row)).with_suffix('.png')

        # create parents
        video_path.parent.mkdir(parents=True, exist_ok=True)

        chain = (
            ffmpeg
                .input(str(input_path))
                .output(str(video_path))
                .overwrite_output()
                .run()
        )

    return 0


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
