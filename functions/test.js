const encoder = require('./encoder.js')


test('get list of bucket', async () => {
    await encoder.filesToEncode('gs://deltares-video-map.appspot.com')
})
