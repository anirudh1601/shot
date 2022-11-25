async function read(){
    var loop = new Date()
    
    // var idata = ctx.getImageData(0,0,1360 ,768);
    
    var canvasData = canvas.toDataURL( "image/jpeg" );
    console.log(canvasData)
    // ffm(canvasData)
    requestAnimationFrame(read)
    // var canvasData = canvas.toDataURL('image/jpeg',1)
    // var decodeAsString = atob(canvasData.split(',')[1])
    // var charArray = []

    // for (var i=0;i<decodeAsString.length;i++){
    //     charArray.push(decodeAsString.charCodeAt(i))
    // }
    // websocket.send(canvasData)
    
}

requestAnimationFrame(read)


// ffmpeg
async function ffm(file){
    console.log(file)
    const { createFFmpeg, fetchFile } = FFmpeg;
    const ffmpeg = createFFmpeg({ log: true });
    const transcode = async ({ target: { file } }) => {
        const { name } = file;
        await ffmpeg.load();
        ffmpeg.FS('writeFile', name, await fetchFile(file));
        await ffmpeg.run('-i', name,  'output.mp4');
    ;}
    document.getElementById('uploader').addEventListener('change', transcode);
}