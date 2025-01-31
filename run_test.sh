docker build . --tag "srt_file_translator" --quiet
docker run -it --rm \
    --volume "$(pwd):/app" \
    "srt_file_translator"

