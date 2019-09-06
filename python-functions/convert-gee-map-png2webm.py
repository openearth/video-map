import os
import subprocess

# vegetation monitor video frame maps are exported using: https://code.earthengine.google.com?scriptPath=users/cindyvdvries/vegetatiemonitor:2019-testing/export-satellite-maps-for-video

# download from storage example:
# gsutil cp -r gs://vegetatiemonitor/classificatie D:/video-map/vegetatiemonitor/

def run(cmd):
    print(cmd)
    subprocess.run(cmd)
# folders = ['classificatie', 'ndvi', 'satellite-false', 'satellite-natural']
bucket_name = "D:/video-map/vegetatiemonitor"
folder = "classificatie"
temp_dir = "temp"
video_folder = folder+"-video"

years = list(range(2000, 2019, 1))
if folder == 'classificatie':
    years.remove(2012)

zoom_levels = range(5, 15, 1)

if not os.path.exists(r'{0}/{1}'.format(bucket_name, temp_dir)):
    os.mkdir(r'{0}/{1}'.format(bucket_name, temp_dir))

new_file_list = []
for y, year in enumerate(years):
    print("Converting year level: {}".format(year))
    for zoom in zoom_levels:
        zoom_dir =  r'{0}/{1}/{2}/{3}'.format(bucket_name, folder, year, zoom)
        tile_x_list = os.listdir(zoom_dir)
        for tile_x in tile_x_list:
            tile_x_dir = r'{0}/{1}'.format(zoom_dir, tile_x)
            tile_y_list = os.listdir(tile_x_dir)
            # move to
            for tile_y in tile_y_list:
                tile_y_dir = r'{0}/{1}'.format(tile_x_dir, tile_y)
                new_path = r'{0}/{1}/{2}/{3}/{4}'.format(bucket_name, temp_dir, zoom, tile_x, tile_y)
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                new_file = r'/{:03d}.png'.format(y+1)
                os.rename(tile_y_dir, new_path+new_file)

for zoom in zoom_levels:
    zoom_dir = r'{0}/{1}/{2}'.format(bucket_name, temp_dir, zoom)
    tile_x_list = os.listdir(zoom_dir)
    for tile_x in tile_x_list:
        tile_x_dir = r'{0}/{1}'.format(zoom_dir, tile_x)
        os.chdir(tile_x_dir)
        tile_y_list = os.listdir(tile_x_dir)
        # move to
        for tile_y in tile_y_list:
            new_path = r'{0}/{1}/{2}/{3}'.format(bucket_name, video_folder, zoom, tile_x)
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            cmd = 'ffmpeg -framerate 5 -i "{0}/{1}/%03d.png" -c:v libvpx -an -qmin 0 -qmax 30 -crf 5 -auto-alt-ref 0 {2}/{1}.webm -y'.format(tile_x_dir, tile_y, new_path)
            run(cmd)

# upload to storage example:
# run("gsutil cp -r D:/video-map/vegetatiemonitor/classificatie-video gs://vegetatiemonitor")
