const encoder = require('./encoder.js')


test('get list of bucket', async () => {
    await encoder.filesToEncode('gs://deltares-video-map-2.appspot.com', prefix='per_year')
})

test('get list of video tiles', async () => {
  let paths = await encoder.filesToEncode('gs://deltares-video-map-2.appspot.com', prefix='per_year')
  paths = paths.map(path => path.name)
  let videoTiles = encoder.videoTiles(paths)
  expect(Object.keys(videoTiles)).toHaveLength(85)
})


test('convert a tile path to an object', () => {
    let path = 'per_year/9/3/7/7.png'
    let tile = encoder.path2Tile(path)
    expect(tile).toHaveProperty('x')
})


test('group files by video tiles', () => {
    let paths = [
        'per_year/0/3/7/7.png',
        'per_year/1/3/7/7.png',
        'per_year/0/3/7/6.png',
        'per_year/1/3/7/6.png'
    ]
    let videoTiles = encoder.videoTiles(paths)
    expect(Object.keys(videoTiles)).toHaveLength(2)
})
