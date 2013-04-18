# -*- coding: utf-8 -*-


def brightness_score(r, g, b):
    '''
    Favours the colors with medium brightness over dark or bright ones
    '''
    # Get the luminance
    # Luminance (perceived option 1)
    x = 0.299 * r + 0.587 * g + 0.114 * b

    # Luminance (standard, objective)
    # x = (0.2126 * r) + (0.7152 * g) + (0.0722 * b)

    # Luminance (perceived option 2, slower to calculate)
    # from math import sqrt
    # x = sqrt(0.241 * r**2 + 0.691 * g**2 + 0.068 * b**2)

    return (-4 * x**2 + 4 * x)


if __name__ == '__main__':
    '''Tests'''
    print 'Good', brightness_score(224/255.0, 27/255.0, 106/255.0)
    print 'Good', brightness_score(35/255.0, 184/255.0, 82/255.0)
    print 'Good', brightness_score(17/255.0, 106/255.0, 184/255.0)

    print 'Bad', brightness_score(172/255.0, 232/255.0, 191/255.0)
    print 'Bad', brightness_score(82/255.0, 78/255.0, 24/255.0)
    print 'Bad', brightness_score(191/255.0, 191/255.0, 191/255.0)
