from taskpaths.process import InputStep
from taskpaths.read import ReadJsonFileStep
from taskpaths.read import StoreAsJsonStep


if __name__ == "__main__":

    process_2 = ReadJsonFileStep(
        "content",
        precedents=[InputStep(id_="file_path", value="data/text_file_stored.json")],
    ) >> StoreAsJsonStep(
        "store_json",
        precedents=[
            InputStep(id_="out_path", value="data/test_file_stored_second.json")
        ],
        indent=10,
    )

    process_2.run()

    print(process_2.value)
