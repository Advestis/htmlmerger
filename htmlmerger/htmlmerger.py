from pathlib import Path
from typing import List, Union, Generator


class HtmlMerger:

    """ Merges html files into a fingle file

    For each file, will extract the content between the <html><body><head> ... <\\head><\\body><\\html> or
    <html><body> ... <\\body><\\html> and put all those contents between those same tags in a new file. Simple as
    that.

    You can either give a list of files or a directory as input, and if not specified the output will be
    input_directory/merged.html, or ./merged.html. You can also pass the argument "clean=True" when calling merge() to
    delete the
    individual files
    used for merging.

    Supports transparentpath objects.

    Examples
    --------

    >>> from htmlmerger import HtmlMerger
    >>> merger = HtmlMerger(input_directory="my_htmls/")  # result will be in my_htmls/merged.html
    >>> merger.merge(clean=True)  # or clean=False to keep the individual files (default behavior)

    >>> from pathlib import Path
    >>> merger = HtmlMerger(files=Path("my_htmls/").glob("*"))  # result will be in ./merged.html
    >>> merger.merge()
    """

    def __init__(
        self,
        files: Union[
            List[Union[Path, str]],
            Generator[Path, None, None],
            Generator[str, None, None],
        ] = None,
        input_directory: Union[Path, str] = None,
        output_path: Union[Path, str] = Path(""),
    ):
        """
        Parameters
        ----------
        files: Union[
            List[Union[Path, str]],
            Generator[Path],
            Generator[str],
        ]
            List or Generator of html files to merge (default value = None).
        input_directory: Union[Path, str]
            Directory containing html files to merge. Alternative to "files" (default value = None).
        output_path: Union[Path, str]
            File in which to save the merged html. (default value = "./merged.html").
        """
        self.files = files
        self.input_directory = input_directory
        self.output_path = output_path
        self.header = ""
        self.tail = ""
        self.contents = {}
        self.loaded = False
        self.check_args()

    def check_args(self):

        if not isinstance(self.input_directory, Path) and self.input_directory is not None:
            self.input_directory = Path(self.input_directory)
        if not isinstance(self.output_path, Path) and self.output_path is not None:
            self.output_path = Path(self.output_path)

        if self.files is None and self.input_directory is None:
            raise AttributeError("Need to specify files or input directory")

        if self.input_directory is not None:
            if self.files:
                raise ValueError("Can not specify both input directory and input files")
            self.files = list(self.input_directory.glob("*.html"))
            self.files.sort()
        
        self.files = [f if not isinstance(f, str) or type(f) == Path else Path(f) for f in
                      self.files]

        if self.output_path is None:
            self.output_path = Path("merged.html")

        if not self.output_path.parent.is_dir():
            raise NotADirectoryError(f"Output directory {self.output_path.parent} not found.")

        self.files = [f for f in self.files if str(f) != str(self.output_path)]

    def get_contents(self):
        first = True
        for file in self.files:
            for line in file.read_text().splitlines():
                if line.startswith("<html>") or line.startswith("<body>") or line.startswith("<head>"):
                    if first:
                        if self.header == "":
                            self.header = line
                        else:
                            self.header = "\n".join([self.header, line])
                    else:
                        continue
                elif line.startswith("</body>") or line.startswith("</html>"):
                    if first:
                        if self.tail == "":
                            self.tail = line
                        else:
                            self.tail = "\n".join([self.tail, line])
                    else:
                        continue
                else:
                    if file.name not in self.contents:
                        self.contents[file.name] = line
                    else:
                        self.contents[file.name] = "\n".join([self.contents[file.name], line])
            first = False
        self.loaded = True

    def merge(self, clean: bool = False):

        if not self.loaded:
            self.get_contents()
        with open(self.output_path, "w") as ofile:
            ofile.write(f"{self.header}\n")
            for name in self.contents:
                ofile.write(f"{self.contents[name]}\n")
            ofile.write(f"{self.tail}")
        if clean:
            self.clean_files()

    def clean_files(self):
        for file in self.files:
            if file.is_file():
                file.unlink()
