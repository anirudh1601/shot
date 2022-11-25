self.importScripts('https://unpkg.com/@ffmpeg/ffmpeg@0.10.0/dist/ffmpeg.min.js')

self.onmessage = async (e) => {
    
    const { createFFmpeg, fetchFile } = FFmpeg;
    const ffmpeg = createFFmpeg({ log: true });
    await ffmpeg.load();
    // await ffmpeg.run('-framerate 30 -pattern_type glob -i /data/thumbnail_*.jpg -c:a copy -shortest -c:v libx264 -pix_fmt yuv420p out.mp4', { outputPath: 'out.mp4' });
    const { data } = await worker.read('out.mp4');
    for (let i = 0; i < cnt; i++) {
        await worker.remove(`thumbnail_${i}.jpg`);
    }
};

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