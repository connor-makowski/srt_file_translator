import codecs, type_enforced, re
from google.cloud import translate_v2 as translate


@type_enforced.Enforcer
class SRT_Utils:
    def parse_srt(
        self, filepath: str, statement_delimiters: list = [".", "?", "!"]
    ):
        """
        Parses an SRT file into a dictionary of statements.
        The keys of the dictionary are the time stamps of the statements.
        The values of the dictionary are the statements themselves.
        Statements that are split across multiple lines are aggregated.

        Arguments:

        * **`filepath`**: `[str]` &rarr; The path to the SRT file to be parsed.
        * **`statement_delimiters`**: `[list]` &rarr; A list of characters that indicate the end of a statement. Defaults to `[".", "?", "!"]`.
        """
        time_structure = re.compile(
            "\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}"
        )

        last_time = "00:00:00,000 --> 00:00:00,000"
        srt_data = {}

        with open(filepath) as filedata:
            for line in filedata:
                line_data = line[:-1]
                if time_structure.match(line_data) is not None:
                    last_time = line_data
                    srt_data[last_time] = []
                else:
                    if last_time not in srt_data:
                        srt_data[last_time] = []
                    srt_data[last_time].append(line_data)
        for key, value in srt_data.items():
            srt_data[key] = " ".join(value[:-1] + [""]).strip()

        srt_data = self.aggregate_statements(
            srt_data=srt_data, statement_delimiters=statement_delimiters
        )
        return srt_data

    def aggregate_statements(self, srt_data: dict, statement_delimiters: list):
        """
        Takes in a dictionary of SRT data and aggregates statements that are split across multiple lines.
        Items are aggregated until a statement delimiter is found at the end of a line.

        Arguments:

        * **`srt_data`**: `[dict]` &rarr; The parsed SRT data.
        * **`statement_delimiters`**: `[list]` &rarr; A list of characters that indicate the end of a statement. Defaults to `[".", "?", "!"]`.

        Returns:

        * **`out_data`**: `[dict]` &rarr; The aggregated SRT data.

        EG:

        ```python

        srt_data = {
            "00:00:00,000 --> 00:00:01,000": "Hello World!",
            "00:00:01,000 --> 00:00:02,000": "This is",
            "00:00:02,000 --> 00:00:03,000": "a test."
        }

        Translator.aggregate_statements(srt_data=srt_data, statement_delimiters=[".", "?", "!"])
        #=> {
        #=>     "00:00:00,000 --> 00:00:01,000": "Hello World!",
        #=>     "00:00:01,000 --> 00:00:03,000": "This is a test."
        #=> }
        """
        data = []
        for key, value in srt_data.items():
            data.append(
                {
                    "start": key.split(" --> ")[0],
                    "end": key.split(" --> ")[1],
                    "string": value,
                }
            )
        merged_data = []
        for idx, item in enumerate(data):
            if len(item["string"]) == 0:
                continue
            if (
                item["string"][-1] in statement_delimiters
                or idx == len(data) - 1
            ):
                merged_data.append(item)
            else:
                data[idx + 1]["string"] = (
                    item["string"] + " " + data[idx + 1]["string"]
                )
                data[idx + 1]["start"] = item["start"]
        out_data = {}
        for item in merged_data:
            out_data[item["start"] + " --> " + item["end"]] = item[
                "string"
            ].strip()
        return out_data

    def write_srt(self, filepath: str, srt_data: dict):
        """
        Writes SRT data to a file.

        Arguments:

        * **`filepath`**: `[str]` &rarr; The path to the SRT file to be written.
        * **`srt_data`**: `[dict]` &rarr; The SRT data to be written to the file.
        """
        idx = 0
        with codecs.open(filepath, "w+", encoding="utf-8-sig") as out_file:
            for key, value in srt_data.items():
                out_file.write(str(idx) + "\n")
                out_file.write(key + "\n")
                out_file.write(value + "\n")
                out_file.write("\n")
                idx += 1


@type_enforced.Enforcer
class Translator(SRT_Utils):
    def __init__(self, key_path: str):
        """
        Initializes the Translator class.

        Arguments:

        * **`key_path`**: `[str]` &rarr; The path to the Google Cloud API key.
            * You can create a key by following the instructions [here](https://cloud.google.com/translate/docs/setup).
        """
        self.__client__ = translate.Client.from_service_account_json(key_path)
        self.__languages__ = self.__client__.get_languages()
        self.__available_languages__ = set(
            [language["language"] for language in self.__languages__]
        )

    def show_languages(self):
        """
        Prints a list of available languages.
        """
        for language in self.__languages__:
            print("{name} ({language})".format(**language))

    def translate(self, text: str, source_language: str, target_language: str):
        """
        Translates a string of text from one language to another.

        Arguments:

        * **`text`**: `[str]` &rarr; The text to be translated.
        * **`source_language`**: `[str]` &rarr; The language of the text to be translated.
        * **`target_language`**: `[str]` &rarr; The language to translate the text to.
        """

        return self.__client__.translate(
            text,
            target_language=target_language,
            source_language=source_language,
        )

    def srt_file_translator(
        self,
        source_file: str,
        target_file: str,
        source_language: str,
        target_language: str,
        statement_delimiters: list = [".", "?", "!"],
    ):
        """
        Reads an SRT file, translates the text, and writes the translated text to a new SRT file.

        Arguments:

        * **`source_file`**: `[str]` &rarr; The path to the SRT file to be translated.
        * **`target_file`**: `[str]` &rarr; The path to the SRT file to be written.
        * **`source_language`**: `[str]` &rarr; The language of the text to be translated.
        * **`target_language`**: `[str]` &rarr; The language to translate the text to.
        * **`statement_delimiters`**: `[list]` &rarr; A list of characters that indicate the end of a statement. Defaults to `[".", "?", "!"]`.
        """
        # General Assertions
        assert (
            source_language in self.__available_languages__
        ), "Source language not supported. Use Translator.show_languages() to see available languages."
        assert (
            target_language in self.__available_languages__
        ), "Target language not supported. Use Translator.show_languages() to see available languages."
        assert source_file.endswith(".srt"), "Source file must be a .srt file"
        assert target_file.endswith(".srt"), "Target file must be a .srt file"

        # Parse SRT
        srt_data = self.parse_srt(
            filepath=source_file, statement_delimiters=statement_delimiters
        )

        # Chunk SRT Data into 128 item chunks
        srt_data_values = list(srt_data.values())
        chunked_values = [
            srt_data_values[i : i + 128]
            for i in range(0, len(srt_data_values), 128)
        ]
        translations = []
        for chunk in chunked_values:
            translations += [
                i["translatedText"]
                for i in self.__client__.translate(
                    chunk,
                    target_language=target_language,
                    source_language=source_language,
                )
            ]
        output_srt_data = dict(zip(srt_data.keys(), translations))
        self.write_srt(filepath=target_file, srt_data=output_srt_data)
