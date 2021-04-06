# encoding: utf-8

import os
import datetime
import cv2
import numpy as np
import pandas as pd
from math import sin, cos, pi
from matplotlib import pyplot


def m00_find_image_bias_and_rad(img, need_show=False):
    """입력받은 단일 수도관 이미지 파일의 Bias를 측정하여
    이를 고려한 이미지 내 중심 초점 픽셀 좌표 및 반경 픽셀 수를 반환합니다."""

    # 이미지 파일의 Array를 Transpose (픽셀 Array 슬라이싱 위치를 맞추기 위함)
    px = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    px[:, :, 0] = img[:, :, 0].T  # Blue Band
    px[:, :, 1] = img[:, :, 1].T  # Green Band
    px[:, :, 2] = img[:, :, 2].T  # Red Band

    # 이미지 파일 중심 및 반경 파악

    # x1 좌표 탐색
    for i in range(200):
        if px[i, 461][0] > 122:  # Check Only Blue Band
            break
    x1 = i
    """cv2.circle(img, (x1, 461), 7, (0, 0, 255), -1)"""

    # x2 좌표 탐색
    for i in range(img.shape[0] - 1 - 200, img.shape[0] - 1):
        if px[i, 461][0] < 122:  # Check Only Blue Band
            break
    x2 = i
    """cv2.circle(img, (x2, 461), 7, (0, 0, 255), -1)"""

    # y1 좌표 탐색
    for j in range(200):
        if px[461, j][0] > 122:  # Check Only Blue Band
            break
    y1 = j
    """cv2.circle(img, (461, y1), 7, (0, 255, 0), -1)"""

    # y2 좌표 탐색
    for j in range(img.shape[1] - 1 - 200, img.shape[1] - 1):
        if px[461, j][0] < 122:  # Check Only Blue Band
            break
    y2 = j
    """cv2.circle(img, (461, y2), 7, (0, 255, 0), -1)"""

    # x1, x2, y1, y2 로부터 중심점 위치 파악
    cx = int((x1 + x2) / 2.0)
    cy = int((y1 + y2) / 2.0)

    # 중심점 타점
    """cv2.circle(img, (cx, 461), 7, (0, 0, 255), -1)
    cv2.circle(img, (461, cy), 7, (0, 255, 0), -1)
    cv2.circle(img, (cx, cy), 7, (255, 255, 255), -1)"""

    # 카메라 Bias 파악
    # x축 기준 Bias 파악
    for k in range(img.shape[0] - 1 - 200, img.shape[0] - 1):
        if px[k, cy][0] < 122:  # Check Only Blue Band
            break
    if not (px[k, cy][0] < 122):
        for k in range(1, 200 + 1):
            if px[k, cy][0] < 122:  # Check Only Blue Band
                break
    if px[k, cy][0] < 122:
        # x축 기준 Bias가 검출된 경우
        tx = k
        """cv2.circle(img, (tx, cy), 7, (255, 0, 0), -1)"""
        # x축 Bias를 고려하여 측정된 반경 픽셀 길이
        imgRad = tx - cx
    # y축 기준 Bias 파악
    else:
        # x축 Bias가 검출되지 않았을 경우
        # y축 기준 Bias 파악
        for j in range(img.shape[1] - 1 - 200, img.shape[1] - 1):
            if px[cx, j][0] < 122:  # Check Only Blue Band
                break
        if not (px[cx, j][0] < 122):
            for j in range(1, 200 + 1):
                if px[cx, j][0] < 122:  # Check Only Blue Band
                    break
        if px[cx, j][0] < 122:  # Check Only Blue Band
            # y축 기준 Bias가 검출된 경우
            ty = j
            """cv2.circle(img, (cx, ty), 7, (255, 0, 0), -1)"""
            # y축 Bias를 고려하여 측정된 반경 픽셀 길이
            imgRad = ty - cy
        else:
            # x축으로도, y축으로도 Bias되지 않은 이미지일 경우
            imgRad = min([img.shape[0] - cx, img.shape[1] - cy])

    # 원이 이미지 밖으로 나가는 것을 방지하기 위한 반경 보정
    if min([cx, cy, px.shape[0] - cx, px.shape[1] - cy, imgRad]) == imgRad:
        # 원 반경 픽셀 수가 이미지 내에 들어오는 경우
        pass
    else:
        # 원 반경 픽셀 수가 이미지 밖으로 나가는 경우
        # >> 중점을 중심으로 수직 방향으로 전후좌우 길이 중 가장 작은 값에서 여유를 두고 픽셀 하나를 더 적게 잡도록 함
        imgRad = min([cx, cy, px.shape[0] - cx, px.shape[1] - cy, imgRad]) - 1

    # Bias, 중점, 반경 파악에 사용된 기준선들 그리기
    """cv2.line(img, (0, 461), (img.shape[0] - 1, 461), (100, 100, 100), 1)
    cv2.line(img, (461, 0), (461, img.shape[1] - 1), (100, 100, 100), 1)
    cv2.line(img, (0, cy), (img.shape[0] - 1, cy), (100, 100, 100), 1)
    cv2.line(img, (cx, 0), (cx, img.shape[1] - 1), (100, 100, 100), 1)"""

    # 중점과 반경에 맞게 원 그리기
    """for i in range(5):
        img = cv2.circle(img, (cx, cy), imgRad - 50 * i, (0, 255, 0), 2)"""

    # 결과 디스플레이
    if need_show:
        # 이미지 저장
        cv2.imwrite(os.path.join(os.path.dirname(img_path),
                                 os.path.basename(img_path).replace(os.path.splitext(os.path.basename(img_path))[-1],
                                                                    '.png')),
                    img)
        cv2.imshow('Biased_Center_Radius', img)
        cv2.waitKey(1000000)
        cv2.destroyAllWindows()

    # Return Biased Center Coordinates and Radius
    return cx, cy, imgRad


def m01_get_polar_fraction(img, cX, cY, rad, dr, theta1, theta2, need_view=False):
    """cX(중심점 x좌표), cY(중심점 y좌표), radius(바깥반경), dr(바깥반경부터 안쪽반경까지 간격),
    theta1(회전각1), theta2(회전각2) 6가지 값에 의해 극좌표계로 정의되는 4개 Point 들을
    이미지 파일 내 직교좌표계로 변환한 결과를 반환합니다."""

    # 입력받은 중점에서 직교하는 직선 축 그리기
    """img = cv2.line(img, (cX, 0), (cX, img.shape[1] - 1), (255, 255, 255), 1)
    img = cv2.line(img, (0, cY), (img.shape[0] - 1, cY), (255, 255, 255), 1)"""

    # Draw Circles
    """for i in range(5):
        img = cv2.circle(img, (cX, cY), rad - 50 * i, (255, 255, 255), 1)"""

    # 내부 반경 구하기
    innerRad = rad - dr

    # 좌상 좌표점
    px1 = int(innerRad * cos(theta1))
    py1 = int(innerRad * sin(theta1))

    # 좌하 좌표점
    px2 = int(rad * cos(theta1))
    py2 = int(rad * sin(theta1))

    # 우상 좌표점
    px3 = int(innerRad * cos(theta2))
    py3 = int(innerRad * sin(theta2))

    # 우하 좌표점
    px4 = int(rad * cos(theta2))
    py4 = int(rad * sin(theta2))

    # Show Points on Image
    if need_view:
        # 좌표점 : 좌상->좌하->우상->우하 (circle 인수 : 이미지, 중심점, 반지름, 색상, 선 두께 및 채우기 옵션)
        cv2.circle(img, (cX + px1, cY - py1), 5, (255, 0, 0), -1)  # Blue
        cv2.circle(img, (cX + px2, cY - py2), 5, (0, 255, 0), -1)  # Green
        cv2.circle(img, (cX + px3, cY - py3), 5, (0, 0, 255), -1)  # Red
        cv2.circle(img, (cX + px4, cY - py4), 5, (0, 255, 255), -1)  # Yellow
        # 이미지 저장
        """cv2.imwrite(os.path.join(os.path.dirname(img_path),
                                 os.path.basename(img_path).replace(os.path.splitext(os.path.basename(img_path))[-1],
                                                                    '.png')),
                    img)"""
        # 뷰어 팝업
        cv2.imshow('PolartPoints', img)
        cv2.waitKey(1000000)
        cv2.destroyAllWindows()

    # 극좌표계에서 4개의 점으로 정의된 영역을 pixel 단위 직교좌표계로 변환한 결과를 return
    return (cX + px1, cY - py1), (cX + px2, cY - py2), (cX + px3, cY - py3), (cX + px4, cY - py4)


def m02_warp_polar_fraction_perspectively(img, in_points, out_width, out_length, need_view=False):
    """이미지 파일 내 4개 포인트(in_points)로 둘러싸인 사각형 영역을
     정의된 너비(out_width)와 높이(out_length) 픽셀을 갖는 직사각형 이미지로 RubberSheeting한 결과를 반환합니다."""

    # 입력받은 4개 Pixel 좌표들을
    inPts = np.float32([[in_points[0][0], in_points[0][1]],
                        [in_points[1][0], in_points[1][1]],
                        [in_points[2][0], in_points[2][1]],
                        [in_points[3][0], in_points[3][1]]])

    # 직사각형 Output 이미지 모서리 좌표 ( 가로 : out_width / 세로 : out_length )
    outPts = np.float32([[0, 0], [0, out_length], [out_width, 0], [out_width, out_length]])

    # RubberSheeting from/to 링크 잡기
    perspT = cv2.getPerspectiveTransform(inPts, outPts)

    # from/to 링크에 따라 RubberSheeting 수행
    warpedImage = cv2.warpPerspective(img, perspT, (out_width, out_length))

    # 확인용 뷰 윈도우 팝업 설정 시 동작
    if need_view:
        # Input 이미지
        inImgToShow = cv2.resize(img, (int(img.shape[1] / 4), int(img.shape[0] / 4)), interpolation=cv2.INTER_CUBIC)
        # 각 좌표점 타점 : 좌상->좌하->우상->우하 (circle 인수 : 이미지, 중심점, 반지름, 색상, 선 두께 및 채우기 옵션)
        cv2.circle(inImgToShow, (int(inPts[0][0] / 4), int(inPts[0][1] / 4)), 5, (255, 0, 0), -1)  # Blue
        cv2.circle(inImgToShow, (int(inPts[1][0] / 4), int(inPts[1][1] / 4)), 5, (0, 255, 0), -1)  # Green
        cv2.circle(inImgToShow, (int(inPts[2][0] / 4), int(inPts[2][1] / 4)), 5, (0, 0, 255), -1)  # Red
        cv2.circle(inImgToShow, (int(inPts[3][0] / 4), int(inPts[3][1] / 4)), 5, (0, 255, 255), -1)  # Yellow
        # Input 이미지를 표시할 뷰어 내 위치 설정
        pyplot.subplot(121)
        pyplot.imshow(inImgToShow)
        pyplot.title('Input')
        # Output 이미지
        pyplot.subplot(122)
        pyplot.imshow(warpedImage)
        pyplot.title('Output')
        # 이미지 뷰어 팝업
        pyplot.show()

    # RubberSheeting 된 이미지를 return
    return warpedImage


def m03_warp_polar_image_perspectively(img, rad, dr, nof_frac, out_length, out_path=''):
    """img_path=파일경로, rad=바깥반경, dr=바깥반경부터 안쪽반경까지 간격, nof_frac=360도를 몇 개 Fraction으로 분할할지,
      out_width=각 fraction 별 가로픽셀 수, out_length=각 fraction 별 세로픽셀 수"""

    # 각 Fraction 별 각도 계산
    tFraction = 2*pi/nof_frac

    # Bias를 고려한 중점 픽셀 좌표와 반경 픽셀 수를 계산
    cx, cy, imgRad = m00_find_image_bias_and_rad(img=img)

    # Bias를 고려한 반경 픽셀 수와 사용자 입력 rad 값 둘 중 작은 것으로 바깥반경을 재정의
    rad = min([rad, imgRad])

    # 반경 값 rad 에 따라 바깥 원 둘레 값을 fraction 수로 나누어 한 조각의 둘레방향 길이를 계산
    circleLenFrac = int(2 * pi * rad / nof_frac)

    # Output 이미지 초기화
    outImg = np.zeros((dr, nof_frac*circleLenFrac, 3), np.uint8)

    # 360도를 72등분한 각 Fraction 별로 RubberSheeting 하고 Output 이미지에 이어 붙이기
    for i in range(nof_frac):
        # 360도를 72등분한 현재 처리중인 마디 내에서 시작 각도와 끝 각도를 계산
        t1 = pi / 2 + tFraction * i
        t2 = t1 + tFraction
        # 360도에서 72등분된 현재 처리중인 마디의 4개 꼭지점 좌표들을 추출
        polarPoints = m01_get_polar_fraction(img=img, cX=cx, cY=cy,
                                             rad=rad, dr=dr, theta1=t1, theta2=t2)
        # 현재 처리중인 마디의 4개 꼭지점 좌표들을 RubberSheet한 결과 이미지를 받는 부분
        fracImg = m02_warp_polar_fraction_perspectively(img=img, in_points=polarPoints,
                                                        out_width=circleLenFrac, out_length=dr)  #
        # RubberSheet된 결과 이미지를 전체 결과에 Paste
        outImg[0:dr, (i * circleLenFrac):((i + 1) * circleLenFrac), 0:3] = fracImg

    # 각 Fraction 들을 이어붙인 결과 Output을 파일로 저장
    # cv2.imwrite(out_path, outImg)

    # 처리 결과 이미지를 Resize
    # >> 이후 메인 작업에서 이 함수가 각 이미지파일마다 반복적으로 실행될 것인데 각 결과를 일정한 해상도로 만들기 위함
    outImgResize = cv2.resize(outImg, (out_length, dr), interpolation=cv2.INTER_CUBIC)

    # RubberSheeting을 통해 펼쳐진 둘레 이미지 resize 결과를 return
    return outImgResize


def m04_loop_warp_and_merge_in_folder_v2(in_dir, out_dir, fileRad, fileDr, nof_frac, fileLen):
    """폴더 내 이미지 파일들을 각각 펼치고 합쳐서 전체 수도관 전개 이미지 제작
    in_dir=INPUT 이미지 폴더 경로, out_dir=OUTPUT 저장 경로, fileRad=각 파일 내 외곽 반경,
    fileDr=각 파일 내 내측 반경으로부터 외곽 반경 사이의 차이,
    nof_frac=각 이미지 파일들을 펼칠 때 360도 각도를 몇등분 하여 작업할지,
    frac_width=극좌표계 기준으로 펼쳐진 조각을 RubberSheeting한 결과 이미지의 너비
    frac_length=극좌표계 기준으로 펼쳐진 조각을 RubberSheeting한 결과 이미지의 높이"""

    # in_dir 폴더 경로 내 모든 파일들을 리스팅
    inImgsPaths = [os.path.join(walk[0], iName) for walk in os.walk(in_dir) for iName in walk[2]]

    # in_dir 폴더 경로 내 모든 파일들의 갯수
    nofFiles = len(inImgsPaths)

    # 이미지 둘레 정보 계산
    circleLenFrac = int(2 * pi * fileRad / nof_frac)
    circleLen = nof_frac * circleLenFrac

    # pasteP, startP, madi 설정
    pasteP = 25
    startP = 10
    madi = 50
    # madi = fileLen - startP

    # Merge Output 이미지 초기화
    mergeImg = np.zeros((fileLen, pasteP*(nofFiles - 1) + madi, 3), np.uint8)

    # 각 이미지 파일별 RubberSheeting 및 전체 결과 한 파일로 Merge
    idx = 0  # 인덱스 변수 초기화
    for imgPath in sorted(inImgsPaths):
        print(imgPath)

        # img 읽어오기
        img = cv2.imread(imgPath)

        # RubberSheeting 결과 이미지
        outImg = m03_warp_polar_image_perspectively(img=img, rad=fileRad, dr=fileDr, nof_frac=nof_frac,
                                                    out_length=fileLen)

        # RubberSheeting 결과 이미지 90도 기울이기
        outImgT = np.zeros((outImg.shape[1], outImg.shape[0], 3), np.uint8)
        outImgT[0:outImg.shape[1], ::-1, 0] = outImg[:, :, 0].T
        outImgT[0:outImg.shape[1], ::-1, 1] = outImg[:, :, 1].T
        outImgT[0:outImg.shape[1], ::-1, 2] = outImg[:, :, 2].T

        # 90도 기울인 RubberSheeting 결과 Output 저장 경로
        outImgPath = os.path.join(out_dir, os.path.basename(in_dir),
                                  os.path.splitext(os.path.basename(imgPath))[0]
                                  + "_{}_{}.jpg".format(str(fileRad - fileDr), str(fileRad)))

        # 90도 기울인 RubberSheeting 결과 Output 저장
        if not os.path.exists(os.path.dirname(outImgPath)):
            os.makedirs(os.path.dirname(outImgPath))
        cv2.imwrite(outImgPath, outImgT)

        # Merge 이미지에 90도 기울인 RubberSheeting 이미지를 이어 붙이기
        # 로그 파일 참고해서 step 을 동적으로 줘야 합니다. >> 6/4 회의에서 로그 파일 시간 참고하지 않기로 결정됨
        mergeImg[:, (pasteP * idx):(pasteP * idx + madi), :] = outImgT[:, startP: (startP + madi), :]
        """if mergeImg.shape[0] == outImgT.shape[0]:
            mergeImg[:, (pasteP * idx):(pasteP * idx + madi), :] = outImgT[:, startP: (startP + madi), :]
        else:
            outImgTResize = cv2.resize(outImgT, (int(outImgT.shape[1] * (circleLen
                                                                         / (outImgT.shape[0] + 1))),
                                                 circleLen),
                                       interpolation=cv2.INTER_CUBIC)
            mergeImg[:, (pasteP * idx):(pasteP * idx + madi), :] = outImgTResize[:, startP: (startP + madi), :]"""

        # 다음 파일로 넘어가면서 인덱스 업데이트
        idx += 1

    # 90도 기울인 RubberSheeting 이미지들 Merge 결과 Output 저장
    mergeImgPath = os.path.join(out_dir, os.path.basename(in_dir),
                                os.path.basename(in_dir) + ".png")
    if not os.path.exists(os.path.dirname(mergeImgPath)):
        os.makedirs(os.path.dirname(mergeImgPath))
    cv2.imwrite(mergeImgPath, mergeImg)


if __name__ == '__main__':

    # Test용 이미지 파일 경로
    testJpgPath = "C:\\Users\\csh\\Documents\\pipe\\python\\pipe_test1.jpg"
    testJpgPath2 = "C:\\Users\\csh\\Documents\\pipe\\test_ori.jpg"

    # Test결과 png 파일 저장 경로
    outPngPath = "C:\\Users\\csh\\Documents\\pipe\\python\\pipe_test1_897_922.png"
    outPngPath2 = "C:\\Users\\csh\\Documents\\pipe\\test_ori_892_922.jpg"

    # Test용 실제 이미지들 폴더 경로
    testJpgsDir = "C:\\Users\\csh\\Documents\\pipe\\20190417\\190417_093634"

    # Test용 실제 이미지들 처리 결과 폴더 경로
    outMergedDir = "C:\\Users\\csh\\Documents\\pipe\\20190417\\190417_093634_out"

    # 속력 계산에 사용될 로그 파일 경로
    testLogPath = "C:\\Users\\csh\\Documents\\pipe\\20190417\\190417_093634.txt"

    # m00_find_image_bias_and_rad Test
    """cx, cy, imgRad = m00_find_image_bias_and_rad(img_path=testJpgPath2, need_show=False)"""

    # m01_get_polar_fraction Test
    """polarPoints = m01_get_polar_fraction(img_path=testJpgPath2, cX=cx, cY=cy,
                                         rad=imgRad-20, dr=100, theta1=pi/4, theta2=pi/4*1.1, need_view=False)
    print("polarPoints = " + str(polarPoints))"""

    # m02_warp_polar_fraction_perspectively Test
    """m02_warp_polar_fraction_perspectively(img_path=testJpgPath2,
                                          in_points=polarPoints, out_width=22, out_length=22*4, need_view=True)"""

    # m03_warp_polar_image_perspectively Test
    """testJpg2 = cv2.imread(testJpgPath2)
    m03_warp_polar_image_perspectively(img=testJpg2, rad=900, dr=88, nof_frac=72*2, out_path=outPngPath2)"""

    # cv2.Stitcher.create() # cv2.Stitcher 클래스 사용법법

   # m04_loop_warp_and_merge_in_folder_v2 Test
    m04_loop_warp_and_merge_in_folder_v2(in_dir=testJpgsDir, out_dir=outMergedDir,
                                         fileRad=926, fileDr=22*1*4,
                                         nof_frac=72*1, fileLen=1584)
