dest=$PWD
cd $( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ffmpeg -i BadAspect_4_1.mp4 -f lavfi -i color=#666666:s=48x12 -f lavfi -i color=black:s=48x12 -f lavfi -i color=white:s=48x12 -ss 7.15 -t 78 -filter_complex scale=48x12,threshold -pix_fmt gray -f rawvideo - | ffmpeg -f rawvideo -pix_fmt gray -s 48x12 -i - -pix_fmt monob -f rawvideo -y $dest/ba.bin
