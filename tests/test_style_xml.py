# ruff: noqa: F403, F405

from functools import partial

from .filecheck_hook import *

t = partial(FileCheckHookTest, hook_id="style-xml")

testdata = [
    t(
        True,
        """<?xml version="1.0" encoding="UTF-8"?>
<foo>
  <bar>test</bar>
</foo>
""",
        """<?xml version="1.0" encoding="UTF-8"?>
<foo>
  <bar>test</bar>
</foo>
""",
        file_name="test.xml",
    ),
    t(
        False,
        """<?xml version="1.0" encoding="UTF-8"?>
<foo>
<bar>test</bar>
</foo>
""",
        """<?xml version="1.0" encoding="UTF-8"?>
<foo>
  <bar>test</bar>
</foo>
""",
        file_name="test.xml",
    ),
    t(
        False,
        """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
<circle cx="50%" cy="50%" r="50%" fill="red"/>
</svg>
""",
        """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
  <circle cx="50%" cy="50%" r="50%" fill="red"/>
</svg>
""",
        file_name="test.svg",
    ),
]


@filecheck_hook_test(testdata)
def test() -> None:
    pass
