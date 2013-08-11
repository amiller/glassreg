import glassreg; from glassreg import *; reload(glassreg)
from transformations import *
import numpy as np
import cv

orientations = \
{"forward":[359.96024,-84.61885,1.8964136],
 "3'oclock":[7.201561,-84.31408,1.7502412],
 "12'oclock":[3.0433965,-89.145325,1.7530643],
 "9'oclock":[1.3155116,-80.02141,2.7109315],
 "6'oclock":[2.1628745,-79.67584,2.1724863],
 "slump right":[356.73083,-80.62881,-30.569677],
 "slump left":[7.4556756,-87.3669,34.312897]}



ormat = \
{"forward":rotation_matrix(np.deg2rad(0), [1,0,0]),
 "12'oclock":rotation_matrix(np.deg2rad(-2), [1,0,0]),
 "6'oclock":rotation_matrix(np.deg2rad(-2), [1,0,0]),
 "3'oclock":rotation_matrix(np.deg2rad(-2), [0,1,0]),
 "9'oclock":rotation_matrix(np.deg2rad(2), [0,1,0]),
 "slump right":rotation_matrix(np.deg2rad(-15), [0,0,1]),
 "slump left":rotation_matrix(np.deg2rad(15), [0,0,1])}


def to_rot(x): 
    rot = matrix_from_vector(np.deg2rad(np.array(x)))
    r = np.empty((3,3))
    r[:3,0] = rot[:3,0]
    r[:3,1] = rot[:3,1]
    r[:3,2] = rot[:3,2]
    return r

def render(name):
    im = cv.LoadImage("clock.png")
    #rinv = np.linalg.inv(to_rot(orientations["forward"]))
    #mrot = to_rot(orientations[name])
    rinv = np.linalg.inv(ormat["forward"][:3,:3])
    mrot = ormat[name][:3,:3]
    print rinv, mrot
    rot = np.dot(mrot,rinv)
    print rot
    homo = homography_from_rotation(rot)
    print homo
    warped = cv.CreateImage((im.width,im.height),8,3)
    cv.WarpPerspective(im, warped, cv.fromarray(homo))
    cv.ShowImage(name, warped)

def once():
    render("forward")
    render("3'oclock")
    render("12'oclock")
    render("slump left")
    render("slump right")
    cv.WaitKey(10)




hBigToGlass = np.array([1.3960742363652061, -0.07945137930533697, -1104.2947209648783, 0.006275578662065556, 1.3523872016751255, -504.1266472917187, -1.9269902737e-05, -9.708578143e-05, 1]).reshape(3,3)
hSmallToBig = np.array([3, 0, 304, 0, 3, 388, 0, 0, 1]).reshape(3,3)
h0 = np.array([1.016551646806814, 0.0103024550424564, -0.004423444927599388,
  -0.005395162051512675, 1.019529659598781, -0.002781452671509211,
  0.0045763927701341, 0.02134943980487344, 1]).reshape(3,3)
h0 = np.ascontiguousarray(np.linalg.inv(h0))
hFinal = np.dot(np.dot(hBigToGlass, hSmallToBig), np.eye(3))

hSmallToBig1 = np.array(
[3.132898564652136, 0.1594935777390666, 280.6367889095118,
  0.03461411915505483, 3.203337447032685, 388.1922957021231,
  5.667899312978336e-05, 0.0001486835346516733, 1]).reshape(3,3)

im = cv.LoadImage("borg_resolution_test.jpg")
im = cv.LoadImage("clock.png");

def warp():
    dst = cv.CreateImage((640,360), 8, 3)
    hFinal = np.dot(np.dot(hBigToGlass, hSmallToBig), h0)
    cv.WarpPerspective(im, dst, cv.fromarray(h0)) #cv.CV_WARP_INVERSE_MAP
    cv.ShowImage("just hMatch01", dst)
    hFinal = np.dot(np.dot(hBigToGlass, hSmallToBig), h0)
    cv.WarpPerspective(im, dst, cv.fromarray(hFinal)) #cv.CV_WARP_INVERSE_MAP
    cv.ShowImage("warped", dst)
    hFinal = np.dot(np.dot(hBigToGlass, hSmallToBig), np.eye(3))
    cv.WarpPerspective(im, dst, cv.fromarray(hFinal)) #cv.CV_WARP_INVERSE_MAP
    cv.ShowImage("with identity", dst)

