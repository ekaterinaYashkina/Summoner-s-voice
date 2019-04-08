class State:
    def __init__(self):
        self.working = False
        self.volume = 0;
        self.enable_advice = True;
        self.enable_healthcare = True;

    def info(self):
        print("System_state:\nWorking: {},\n Volume: {}, \n Advice: {}, \n healthCare: {}, \n".format(self.working, self.volume, self.enable_advice, self.enable_healthcare))