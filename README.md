# ssal_calc
- 메이플 피로도 당 재획비, 경축비, 소형재획비 효율 계산기 입니다.

- 각 효율은 피로도 500을 모두 태운 것을 기준으로 함
- Python 3.12.10

```python
pip install pyinstaller
pip install ttkbootstrap

pyinstaller --onefile --windowed main.py # build
pyinstaller --onefile --noconsole --icon="icons/icon.ico" --add-data="icons;icons" main.py # only windows
```

- buil 해서 /dist 내부 exe 파일을 실행시키면 됩니다.
