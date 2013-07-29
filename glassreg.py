
f = 2968.5
cx = 640/2
cy = 360/2

# image coordinate = KK * direction vector
KK = [[f, 0, cx],
      [0, f, cy],
      [0, 0,  1]]

# direction vector = KK_inv * image coordinate
invKK = np.linalg.inv(KK)

def homgraphy_from_rotation(rot):
    # multiply out matrix 3 times
    return np.dot(KK, np.dot(rot, invKK))

def apply_rotation(rot, p):
    # p is a homogeneous image point ~ (x,y,1)
    direction_vector = np.dot(invKK, p)
    rotated_direction = np.dot(rot, direction_vector)
    p_prime = np.apply(KK, rotated_direction)
    return p_prime

# For improving the rotation matrix
orientation_fwd = np.array([281.16583,-87.140755,2.3037903])/360
orientation_right = np.array([1.9436421,-86.628334,1.443224])/360

def matrix_from_vector((q1,q2,q3)):
    q0 = 1 - q1*q1 - q2*q2 - q3*q3;
    q0 = np.sqrt(q0) if q0 > 0 else 0

    sq_q1 = 2 * q1 * q1
    sq_q2 = 2 * q2 * q2
    sq_q3 = 2 * q3 * q3
    q1_q2 = 2 * q1 * q2
    q3_q0 = 2 * q3 * q0
    q1_q3 = 2 * q1 * q3
    q2_q0 = 2 * q2 * q0
    q2_q3 = 2 * q2 * q3
    q1_q0 = 2 * q1 * q0

    R = np.empty((3,3))
    R[0,0] = 1 - sq_q2 - sq_q3;
    R[0,1] = q1_q2 - q3_q0;
    R[0,2] = q1_q3 + q2_q0;

    R[1,0] = q1_q2 + q3_q0;
    R[1,1] = 1 - sq_q1 - sq_q3;
    R[1,2] = q2_q3 - q1_q0;

    R[2,0] = q1_q3 - q2_q0;
    R[2,1] = q2_q3 + q1_q0;
    R[2,2] = 1 - sq_q1 - sq_q2;

    return R

