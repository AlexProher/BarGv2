

class TwoDimVec:
    def __init__(self, x=[], y=[]):
        self.x = x
        self.y = y

    def copy_from_two_dim_array(self, array):
        for i in range(len(array)):
            try:
                self.y.append(float(array[i][0]))
                self.x.append(float(array[i][1]))

            except Exception as exception:
                print(exception)
        return self

    def force_signal_to_start_at_zero(self):
        zeroing([self.x, self.y])
        return self

    def create_absolute_copy(self, twoDimVec):
        self.x = twoDimVec.x.copy()
        self.y = twoDimVec.y.copy()
        return self

    def crop_until_index(self, i):
        self.x = self.x[:i]
        self.y = self.y[:i]

    def crop_from_index(self, i):
        self.x = self.x[i:]
        self.y = self.y[i:]


def zeroing(signals):
    """
            Not all experiments are born perfect, and some might be entirely offset.
            Thus, we can take the first value of each vector and move the entire
            vector upwards or downwards by that value
            (in an ideal experiment the first value will be 0).
    """

    for signal in signals:
        zeroer = signal[0]
        for i in range(len(signal)):
            signal[i] -= zeroer