import streamlit as st

st.write("""Streamlit supports markdown syntax. For example, you can write math equations like this: $y = x^2$
Or **bold** and *italic* and ***bold and italic*** text. You can also create tables:
| Syntax | Description |
| ----------- | ----------- |
| Header | Title |
| Paragraph | Text |


You can also create headers:
# Header 1
## Header 2
### Header 3
#### Header 4

Here is an unordered list:
- Item 1
- Item 2
- Item 3

Here is an ordered list:
1. Item 1
2. Item 2

Code blocks are also supported:
```python
import streamlit as st
st.write("Hello world!")
```

Emojis are also supported: 
:smile: :smiley: :wink: :disappointed:  :angry: :cry: :heart_eyes: :confused: :astonished:
:heart: :star: :warning: :lock: :unlock: :calendar: :alarm_clock: :watch:
:mag: :sound: :speaker: :mute: :camera: :computer: :hourglass: :battery:
:arrow_forward: :fast_forward: :rewind: :eject:
:thumbsup: :thumbsdown: :white_check_mark: :x: :heavy_plus_sign: :heavy_minus_sign:
:arrow_right: :arrow_left: :arrow_up: :arrow_down:

Links are also supported: [Streamlit](https://streamlit.io/)
<petri.kuittinen@hamk.fi>
<https://hamk.fi/>

Images are only supported as URLs:
![Streamlit logo](https://streamlit.io/images/brand/streamlit-mark-color.png)
or your could base64 encode the image and give as data URL.
""")
st.write(r"More math, need raw strings $$ x = {-b \pm \sqrt{b^2-4ac} \over 2a} $$")
