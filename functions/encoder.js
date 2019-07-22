// Imports the Google Cloud client library
const {Storage} = require('@google-cloud/storage');

const firestore = require('firebase/firestore')
const _  = require('lodash')

const ffmpegPath = require('@ffmpeg-installer/ffmpeg').path
const FfmpegCommand = require('fluent-ffmpeg')
FfmpegCommand.setFfmpegPath(ffmpegPath)
const fs = require('fs')
const path = require('path')
const stream = require('stream')
const multer = require('multer')
const storage = multer.memoryStorage()

const tileRegexp =  /^(.*)\/(\d+)\/(\d+)\/(\d+)\/(\d+)(\.\w+)$/

function path2Tile(path) {
    // split  the path into a tile object
    let result = tileRegexp.exec(path)
    if (!result) {
        return result
    }
    let prefix = result[1]
    let frame = result[2]
    let zoom = result[3]
    let x = result[4]
    let y = result[5]
    let suffix = result[6]
    return {
        path,
        prefix,
        frame,
        zoom,
        x,
        y,
        suffix
    }
}
async function filesToEncode(bucketName, prefix='', suffix='') {
    // Lists files in the bucket
    
    // Creates a client
    const storage = new Storage()
    // Get all the files  that start with prefix
    // I don't know what this syntax  means
    let [files] = await storage.bucket(bucketName).getFiles({prefix})
    // Filter by suffix
    
    files = files.filter(file => {
        let result = file.name.endsWith(suffix)
        return result
    })
    return files
}

function videoTiles(files) {
    let tiles = files.map(path2Tile)
    // todo, warn  if  we  filtered out something
    tiles = tiles.filter(x => x)
    let grouped = _.groupBy(tiles, (tile) => {
        return [tile.zoom, tile.x, tile.y]
    })
    return grouped
}

class WritableChunkCache extends stream.Writable {

    constructor(options) {
        super(options)
        this._chunks = []
    }

    write(chunk, encoding, callback) {
        this._chunks.push(chunk)
        if(typeof callback === 'function') {
            return callback()
        }
    }

    writev(chunks, callback) {
        this._chunks = this._chunks.concat(chunks)
        if(typeof callback === 'function') {
            return callback()
        }
    }

    get buffer(){
        return Buffer.concat(this._chunks)
    }
}

 function encodeVideoMapTiles(req, res){

    // handle multipart form data
    var videoUpload = mult.single('video')
    videoUpload(req, res, () => {

        var file = req.file
        var readStream = new stream.PassThrough()
        readStream.end(new Buffer(file.buffer))
        var outStream = new WritableChunkCache()

        var command = new FfmpegCommand(readStream)
            .fps(30)
            .on('end', () => {
                res.send({buffer: outStream.buffer})
            })
            .on('error', (err, ...args) => {
                console.error(err, args)
                res.send(err)
            })
            .format('mp4')
            .videoCodec('libx264')
            .outputOptions([
                '-movflags frag_keyframe+empty_moov' // accounting for unknown duration due to streamed input
            ])
            .pipe(outStream, { end: true })
    })
}

module.exports = {
    encodeVideoMapTiles,
    filesToEncode,
    path2Tile,
    videoTiles
}
