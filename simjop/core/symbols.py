import datetime
import tempfile
import jinja2
import wx

from core.symbol_constants import SymbolType, SymbolMode


class Symbols:
    def __init__(self):
        self._matrix = []
        self._symbols = {}
        self._create_symbols()

    def _create_matrix(self):
        for symbol in SymbolType:
            filename = f"{str(symbol).replace('SymbolType.', '').lower()}.svg"
            for mode in SymbolMode:
                item = {
                    "template": filename,
                    "symbol": f"{symbol}.{mode}",
                }
                match mode:
                    case SymbolMode.DEFAULT:
                        item["params"] = {"color": "grey"}
                    case SymbolMode.HELPER:
                        item["params"] = {"color": "yellow"}
                    case _:
                        pass

                self._matrix.append(item)

    def _create_symbols(self):

        now = datetime.datetime.now()
        self._create_matrix()

        jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(searchpath="./simjop/templates"),
            autoescape=jinja2.select_autoescape(),
        )

        with tempfile.TemporaryDirectory() as tmp_dirname:
            for pattern in self._matrix:
                with tempfile.NamedTemporaryFile(
                    mode="w", dir=tmp_dirname, delete=False
                ) as tmp_file:
                    template = jinja_env.get_template(pattern["template"])
                    template.stream(pattern["params"]).dump(tmp_file.name)
                    self._symbols[pattern["symbol"]] = wx.Bitmap(
                        tmp_file.name, wx.BITMAP_TYPE_ANY
                    )

        delta = datetime.datetime.now() - now
        print("Bitmaps generated in: ", delta)  # TODO

    def bitmap(self, symbol, mode):
        key = f"{symbol}.{mode}"
        # TODO: Is key in the matrix?
        return self._symbols[key]
