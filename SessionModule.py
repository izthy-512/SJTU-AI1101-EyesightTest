import random
from HandTrackingModule import HandDetector
from MyTimer import MyTimer

class Session:

    INTERVAL_SESSION = 8
    INTERVAL_CONFIRM = 2
    INTERVAL_PAUSE = 1

    def __init__(self):
        
        self.timer_session = MyTimer(interval=self.INTERVAL_SESSION)
        self.timer_confirm = MyTimer(interval=self.INTERVAL_CONFIRM, function=self.timer_session.cancel)
        self.timer_pause = MyTimer(interval=self.INTERVAL_PAUSE)
        
        self.result = False
        self.handDetector = HandDetector()

    def update(self, stage):

        self.stage = stage
        while self.timer_pause.is_alive():
            pass
        self.sign_direction = random.randint(1, 4)                       # 'E'朝向
        self.hand_direction = None

    def start(self):

        self.timer_session.start()

        while self.timer_session.is_alive():

            hand_direction = self.handDetector.findDirection()

            # 若检测到方向并且与记录一致，启动确认倒计时
            if hand_direction and hand_direction == self.hand_direction:
                if not self.timer_confirm.is_alive():
                    self.timer_confirm.start()
            else:
                self.timer_confirm.cancel()
            
            self.hand_direction = hand_direction
        
        self.result = (self.sign_direction == self.hand_direction)

        self.timer_pause.start()
