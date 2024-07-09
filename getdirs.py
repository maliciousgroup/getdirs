from urllib.parse import urlparse
from pathlib import Path

#
# getdirs.py - written by d3d @deadvolvo 2022
#


class GetDirs(object):
    def __init__(self, i_file: str, o_file: str, i_stdin: bool, b_list: str, w_list: str):
        self.i_file: list = self.return_list(i_file)
        self.b_list: list = self.return_list(b_list)
        self.w_list: list = self.return_list(w_list)
        self.i_stdin: list = self.return_stdin(i_stdin)
        self.urls: list = list(set(self.i_file + self.i_stdin))
        self.o_file: str = o_file

    @staticmethod
    def return_list(filename: str) -> list:
        if not filename or filename.rstrip() == '':
            return []
        return [x.rstrip() for x in open(filename, encoding='utf8')] if Path(filename).is_file() else [filename]

    @staticmethod
    def return_stdin(use_stdin: bool) -> list:
        return [x.rstrip() for x in sys.stdin.readlines() if use_stdin]

    @staticmethod
    def write_list_to_file(filename: str, content: list) -> None:
        try:
            with open(f"{filename}", 'a') as file:
                file.write("\n".join(content))
        except OSError as e:
            print(f"Error occurred when writing to file: {e.__str__()}.\n")

    @staticmethod
    def parse_urls(data: list) -> list:
        urls: list = []
        for line in data:
            o = urlparse(line)
            path = o.path.split('/')[1:-1]
            for x in range(len(path)):
                temp_url = f"{o.scheme}://{o.netloc}/{'/'.join(path[0:x + 1])}/"
                urls.append(temp_url)
        return urls

    def main(self):
        urls: list = []
        if self.b_list:
            [urls.append(url) for url in self.urls if not any(x in url for x in self.b_list)]

        if self.w_list:
            [urls.append(url) for url in self.urls if any(x in url for x in self.w_list)]

        if not self.b_list and not self.w_list:
            urls = self.urls

        dirs = list(set(self.parse_urls(urls)))

        if self.o_file:
            self.write_list_to_file(self.o_file, dirs)
        else:
            print('\n'.join(dirs))


def usage() -> None:
    output: str = f"""Options:
  '-f', '--file'        - Set the file containing URLS with directories you want to parse
  '-s', '--stdin'       - Set the stdin flag to enable piping data directly to the application
  '-o', '--output'      - Set the output filename and location to store results
  '-b', '--blacklist'   - Set the domain or file containing blacklisted domains to skip
  '-w', '--whitelist'   - Set the domain or file containing whitelisted domains use

"""
    print(output)


if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser(add_help=False, usage=None)
    parser.add_argument('-f', '--file', action='store', dest='i_file', type=str, default='', required=False)
    parser.add_argument('-s', '--stdin', action='store_true', dest='i_stdin', default=False, required=False)
    parser.add_argument('-o', '--output', action='store', dest='o_file', type=str, default='', required=False)
    parser.add_argument('-b', '--blacklist', action='store', dest='w_list', type=str, default='', required=False)
    parser.add_argument('-w', '--whitelist', action='store', dest='b_list', type=str, default='', required=False)
    arg = None

    try:
        arg = parser.parse_args()
        if arg.i_file == '' and arg.i_stdin is False:
            raise TypeError
        getdirs = GetDirs(arg.i_file, arg.o_file, arg.i_stdin, arg.w_list, arg.b_list)
        getdirs.main()
    except TypeError:
        exit(usage())
