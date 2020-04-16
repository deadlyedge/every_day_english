from datetime import datetime


class InfoBox:
    def __init__(self):
        self.date = datetime.now()


if __name__ == '__main__':
    ib = InfoBox()
    print(ib.date)
