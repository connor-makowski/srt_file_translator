import codecs, type_enforced, re
from google.cloud import translate_v2 as translate


@type_enforced.Enforcer
class SRT_Utils:
    def parse_srt(
        self, filepath: str, statement_delimiters: list = [".", "?", "!"]
    ):
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
        srt_data = self.aggregate_statements(
            srt_data=srt_data, statement_delimiters=statement_delimiters
        )
        return srt_data

    def aggregate_statements(self, srt_data: dict, statement_delimiters: list):
        data = []
        for key, value in srt_data.items():
            raw_string = " ".join(value[:-1] + [""])
            data.append(
                {
                    "start": key.split(" --> ")[0],
                    "end": key.split(" --> ")[1],
                    "string": raw_string.strip(),
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
        self.__client__ = translate.Client.from_service_account_json(key_path)
        self.__languages__ = self.__client__.get_languages()
        self.__available_languages__ = set(
            [language["language"] for language in self.__languages__]
        )

    def show_languages(self):
        for language in self.__languages__:
            print("{name} ({language})".format(**language))

    def translate(self, text: str, source_language: str, target_language: str):
        return self.__client__.translate(text, target_language=target_language)

    def translate_srt(
        self,
        source_file: str,
        target_file: str,
        source_language: str,
        target_language: str,
    ):
        # General Assertions
        assert (
            source_language in self.__available_languages__
        ), "Source language not supported"
        assert (
            target_language in self.__available_languages__
        ), "Target language not supported"
        assert source_file.endswith(".srt"), "Source file must be a .srt file"
        assert target_file.endswith(".srt"), "Target file must be a .srt file"

        # Parse SRT
        srt_data = self.parse_srt(filepath=source_file)
        translations = [
            i["translatedText"]
            for i in self.__client__.translate(
                list(srt_data.values()), target_language=target_language
            )
        ]
        output_srt_data = dict(zip(srt_data.keys(), translations))
        self.write_srt(filepath=target_file, srt_data=output_srt_data)
