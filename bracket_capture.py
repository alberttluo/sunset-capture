import cv2
import time
import numpy as np

def hdr(curr_time, dir):
    GOOD_AVERAGE = 50

    cam = cv2.VideoCapture(0)
    # cam.set(cv2.CAP_PROP_FRAME_WIDTH, 2592)
    # cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1944)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)
    cam.set(cv2.CAP_PROP_GAIN, 0.5)

    cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    # loop exposure to find the good exposure time
    good_exp = 0
    for exp in range(60):
        cam.set(cv2.CAP_PROP_EXPOSURE, exp*10)
        for i in range(4):
            ret, frame = cam.read()    

        # exp_r = cam.get(cv2.CAP_PROP_EXPOSURE)
        print(f"write exp = {exp}")
        ret, frame = cam.read()
        if ret:
            average = np.mean(frame)
            print(f"average = {average},, exp = {exp*10}")
            if average > GOOD_AVERAGE:
                good_exp = exp*10
                break


    # capture 3 frames
    img_list = []
    exp_list = [good_exp/2, good_exp, good_exp*2]
    for exp in exp_list:
        cam.set(cv2.CAP_PROP_EXPOSURE, exp)
        for i in range(4):
            ret, frame = cam.read()    

        ret, frame = cam.read()
        filename = dir + '/' + curr_time + ' exp ' + str(exp) + '.jpg'
        if ret:
            print(f"capture one frame at exposure = {exp} filename = {filename}")
            #cv2.imwrite(filename, frame)
            img_list.append(frame)

    cam.release()

    exposure_times = np.array(exp_list, dtype=np.float32)
    # Merge exposures to HDR image
    merge_debevec = cv2.createMergeDebevec()
    hdr_debevec = merge_debevec.process(img_list, times=exposure_times.copy())
    merge_robertson = cv2.createMergeRobertson()
    hdr_robertson = merge_robertson.process(img_list, times=exposure_times.copy())
    # Tonemap HDR image
    tonemap1 = cv2.createTonemap(gamma=2.2)
    res_debevec = tonemap1.process(hdr_debevec.copy())
    # Exposure fusion using Mertens
    merge_mertens = cv2.createMergeMertens()
    res_mertens = merge_mertens.process(img_list)
    # Convert datatype to 8-bit and save
    res_debevec_8bit = np.clip(res_debevec*255, 0, 255).astype('uint8')
    res_mertens_8bit = np.clip(res_mertens*255, 0, 255).astype('uint8')
    hdr1file = dir + '/' + curr_time + ' hdr_debevec.jpg'
    hdr2file = dir + '/' + curr_time + ' hdr_fusion.jpg'
    cv2.imwrite(hdr1file, res_debevec_8bit)
    cv2.imwrite(hdr2file, res_mertens_8bit)