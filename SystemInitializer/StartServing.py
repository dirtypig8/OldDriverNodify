from threading import Thread
from SpiderMaintinaer.AvLineBot import AvLineBot


class StartServing:
    def execute(self):
        InitializeAvLineBot().execute()


class InitializeAvLineBot:
    @staticmethod
    def execute():
        Avbot = AvLineBot()
        Avbot.update_sources()
        Thread(
            target=Avbot.execute
        ).start()

        Thread(
            target=Avbot.get_new_avid
        ).start()




