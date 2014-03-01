import matplotlib
matplotlib.use('wx')
import pylab
import json
import sys

def click_points(n, im):
    fig = pylab.figure(1);
    pylab.imshow(im)

    def pick(event):
        points.append((event.xdata, event.ydata))
        print('Picked point %d of %d' % (len(points),n))

    fig.canvas.mpl_connect('close_event', lambda _: sys.exit(1))
    cid = fig.canvas.mpl_connect('button_press_event', pick)
    points = []
    print("Click %d points" % (n,))

    while len(points) < n:
        pylab.waitforbuttonpress()

    print "Ok!", points

if __name__ == '__main__':
    import cv2
    click_points(5, cv2.imread('clock.png'))
