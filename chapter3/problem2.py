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


from chapter3.problem1 import sigmoid
import numpy as np
import logging


__author__ = 'Junya Kaneko <jyuneko@hotmail.com>'


class ProbabilisticElement:
    def __init__(self, w, alpha, theta):
        self._w = w if isinstance(w, np.ndarray) else np.array(w)
        self._alpha = alpha
        self._theta = theta

    def out(self, input, alpha=None, theta=None):
        _input = input if isinstance(input, np.ndarray) else np.array(input)
        _alpha = alpha if alpha else self._alpha
        _theta = theta if theta else self._theta
        logging.debug('PARAMETERS (alpha, theta): (%s, %s)' % (_alpha, _theta))
        logging.debug('INPUT: (%s), SIGMOID: %s' % (','.join([str(i) for i in _input]), sigmoid(self._w.dot(_input), _alpha, _theta)))
        if np.random.rand(1, 1) < sigmoid(self._w.dot(_input), _alpha, _theta):
            logging.debug('OUTPUT: %s' % 1)
            return 1
        else:
            logging.debug('OUTPUT: %s' % 0)
            return 0

    def __call__(self, input, alpha=None, theta=None):
        return self.out(input, alpha, theta)


if __name__ == '__main__':
    #logging.basicConfig(level=logging.DEBUG)

    w = np.array([3, 2, 1])
    alpha = 1
    theta = 1
    p_element = ProbabilisticElement(w, alpha, theta)

    num_of_loops = 50000

    for i in [[1, 0, 1], [1, -1, 0], ]:
        num_of_ones = 0
        for l in range(0, num_of_loops):
            if p_element(i):
                num_of_ones += 1
        probability = num_of_ones / num_of_loops

        print('Sigmoid: ', sigmoid(w.dot(i), theta=theta))
        print('Probability of one: ', probability)
        assert np.round(probability, 2) == np.round(sigmoid(w.dot(i), theta=theta), 2)
