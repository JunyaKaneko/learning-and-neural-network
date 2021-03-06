# This file is part of "Junya's self learning project about Neural Network."
#
# "Junya's self learning project about Neural Network"
# is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# "Junya's self learning project about Neural Network"
# is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
# (c) Junya Kaneko <jyuneko@hotmail.com>


import numpy as np
from matplotlib import pyplot
from time import time


__author__ = 'Junya Kaneko <jyuneko@hotmail.com>'


class Learner:
    """
    線形近似を行う(y = ax の a を求める)学習器。
    """
    def __init__(self, a, da=0.01, epsilon=0.01, nsteps=1000):
        self._a = a
        self._da = da
        self._epsilon = epsilon
        self._nsteps = nsteps
        self._learning_time = 0

    @property
    def learning_time(self):
        return self._learning_time

    def _get_error(self, data, a):
        return np.array([np.power(x[1] - a * x[0], 2) for x in data]).sum()

    def get_error(self, data):
        return self._get_error(data, self._a)

    def learn(self, data):
        prev_e = np.infty
        start = time()
        for s in range(self._nsteps):
            de = (self._get_error(data, self._a) - self._get_error(data, self._a + self._da)) / self._da
            a = self._a + self._epsilon * de
            e = self._get_error(data, a)
            if e >= prev_e:
                self._learning_time = time() - start
                return True
            else:
                self._a = a
                prev_e = e
        return False

    def get_value(self, x):
        return self._a * x


if __name__ == '__main__':
    # 学習に使用するデータ
    data = np.array([[1, 1], [2, 2.5], [3, 2.5], [4, 4.5], [5, 4.5]])

    # 一括学習用の学習器 b_learner と 逐次学習器 s_learner
    b_learner = Learner(1)
    s_learner = Learner(1)

    # 一括学習
    b_success = b_learner.learn(data)

    # 逐次学習
    s_success = False
    s_learning_times = []
    for datum in data:
        s_success = s_learner.learn([datum, ])
        if s_success:
            s_learning_times.append(s_learner.learning_time)
            s_success = True
        else:
            s_success = False
            break

    # 一括学習と逐次学習が両方とも成功している場合に
    # 求めた近似式のグラフ、学習速度、エラーの大きさ、をグラフ表示
    if b_success and s_success:
        x1, x2 = np.hsplit(data, 2)

        pyplot.subplot(3, 1, 1)
        pyplot.scatter(x1, x2, label='Actual data')
        pyplot.plot(x1, [b_learner.get_value(x) for x in x1], label='Batch')
        pyplot.plot(x1, [s_learner.get_value(x) for x in x1], label='Sequential')
        pyplot.title('Actual data and approx line')
        pyplot.xlabel('x1')
        pyplot.ylabel('x2')
        pyplot.legend(loc="upper left")

        pyplot.subplot(3, 1, 2)
        pyplot.bar([0, 1], [b_learner.learning_time, np.array(s_learning_times).sum()], align='center', width=0.4)
        pyplot.title("Batch's and sequential's learning time")
        pyplot.xticks([0, 1], ['Batch', 'Sequential'])

        pyplot.subplot(3, 1, 3)
        pyplot.bar([0, 1], [b_learner.get_error(data), s_learner.get_error(data)], align='center', width=0.4)
        pyplot.title("Batch's and sequential's sum of square root error")
        pyplot.xticks([0, 1], ['Batch', 'Sequential'])

        pyplot.tight_layout()
        pyplot.show()
