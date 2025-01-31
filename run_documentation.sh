# Change to the script directory
cd $(dirname "$0")
# Ensure a properly setup virtual environment
printf "Setting up the virtual environment..."
python3 -m virtualenv venv > /dev/null
source venv/bin/activate
# If not in an venv, do not continue
if [ -z "$VIRTUAL_ENV" ]; then
    printf "\nNot in a virtual environment. Exiting."
    exit 1
fi
pip install -r requirements.txt > /dev/null
printf "done.\n"
# Make a temp init.py that only has the content below the __README_CONTENT_IS_COPIED_ABOVE__ line
cp README.md srt_file_translator/__init__.py
sed -i '1s/^/\"\"\"\n/' srt_file_translator/__init__.py
echo "\"\"\"" >> srt_file_translator/__init__.py
echo "from .translator import Translator, SRT_Utils" >> srt_file_translator/__init__.py


# Specify versions for documentation purposes
VERSION="1.0.1"
OLD_DOC_VERSIONS="1.0.0"
export version_options="$VERSION $OLD_DOC_VERSIONS"

# generate the docs for a version function:
function generate_docs() {
    INPUT_VERSION=$1
    if [ $INPUT_VERSION != "./" ]; then
        if [ $INPUT_VERSION != $VERSION ]; then
            pip install "./dist/srt_file_translator-$INPUT_VERSION.tar.gz"
        fi
    fi
    python3 -m pdoc -o ./docs/$INPUT_VERSION -t ./doc_template srt_file_translator
}

# Generate the docs for the current version
generate_docs ./
generate_docs $VERSION

# Generate the docs for all the old versions
for version in $OLD_DOC_VERSIONS; do
    generate_docs $version
done;

# Reinstall the current package as an egg
pip install -e .
