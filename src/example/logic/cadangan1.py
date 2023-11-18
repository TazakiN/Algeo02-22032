from PIL import Image
import numpy as np
import time

def ImagetoRGB(path):  # input merupakan alamat atau path dari image
    image = Image.open(path)
    image_array = image.convert("RGB")
    # image_array = np.array(image_array).astype(np.float32)
    # return image_array
    image_array = np.array(image_array)
    return image_array
    

def cosine(A, B):
    return (np.dot(A, B) / (np.linalg.norm(A) * np.linalg.norm(B))) * 100


def convert_rgb_hsv(path_gambar):
    # Ganti path_gambar dengan path foto yang ingin Anda ubah

    matrix_rgb = ImagetoRGB(path_gambar)
    hsv = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # v = np.max(rgb_normalized, axis=2)
    # h = np.where(
    #     (v == r), 60 * ((g - b) / delta % 6),
    #     np.where((v == g), 60 * ((b - r) / delta + 2),
    #              60 * ((r - g) / delta + 4)))
    matrix_rgb = matrix_rgb/255.0
    
    # for i in range(len(matrix_rgb)):    
    #     for j in range(len(matrix_rgb[i])):
    #         cmin = 1
    #         cmax = 0
            
    #         for k in range (3):
               
    #             if(matrix_rgb[i][j][k]>=cmax):
                    
    #                 cmax = matrix_rgb[i][j][k]
    #                 if j == 0:
    #                     indikatormax = 0
    #                 elif j == 1:
    #                     indikatormax = 1
    #                 else:
    #                     indikatormax = 2

    #             if matrix_rgb[i][j][k] <= cmin:
    #                 cmin = matrix_rgb[i][j][k]

    #         delta = cmax - cmin

    #         if delta == 0:
    #             matrix_rgb[i][j][0] = 0
    #         elif indikatormax == 0:
    #             matrix_rgb[i][j][0] = 60 * (
    #                 ((matrix_rgb[i][j][1] - matrix_rgb[i][j][2]) / delta) % 6
    #             )
    #         elif indikatormax == 1:
    #             matrix_rgb[i][j][0] = 60 * (
    #                 ((matrix_rgb[i][j][2] - matrix_rgb[i][j][0]) / delta) + 2
    #             )
    #         else:
    #             matrix_rgb[i][j][0] = 60 * (
    #                 ((matrix_rgb[i][j][0] - matrix_rgb[i][j][1]) / delta) + 4
    #             )

    #         matrix_rgb[i][j][0] = round(matrix_rgb[i][j][0])

    #         if cmax == 0:
    #             matrix_rgb[i][j][1] = 0
    #         else:
    #             matrix_rgb[i][j][1] = delta / cmax

    #         matrix_rgb[i][j][2] = cmax

    #         if (matrix_rgb[i][j][0] >= 316) and (matrix_rgb[i][j][0] <= 360):
    #             h[0] += 1
    #         elif (matrix_rgb[i][j][0] >= 1) and (matrix_rgb[i][j][0] <= 25):
    #             h[1] += 1
    #         elif (matrix_rgb[i][j][0] >= 26) and (matrix_rgb[i][j][0] <= 40):
    #             h[2] += 1
    #         elif (matrix_rgb[i][j][0] >= 41) and (matrix_rgb[i][j][0] <= 120):
    #             h[3] += 1
    #         elif (matrix_rgb[i][j][0] >= 121) and (matrix_rgb[i][j][0] <= 190):
    #             h[4] += 1
    #         elif (matrix_rgb[i][j][0] >= 191) and (matrix_rgb[i][j][0] <= 270):
    #             h[5] += 1
    #         elif (matrix_rgb[i][j][0] >= 271) and (matrix_rgb[i][j][0] <= 295):
    #             h[6] += 1
    #         elif (matrix_rgb[i][j][0] >= 295) and (matrix_rgb[i][j][0] <= 315):
    #             h[7] += 1

    #         if (matrix_rgb[i][j][1] >= 0) and (matrix_rgb[i][j][1] < 0.2):
    #             h[8] += 1
    #         elif (matrix_rgb[i][j][1] >= 0.2) and (matrix_rgb[i][j][1] < 0.7):
    #             h[9] += 1
    #         elif (matrix_rgb[i][j][1] >= 0.7) and (matrix_rgb[i][j][1] <= 1):
    #             h[10] += 1

    #         if (matrix_rgb[i][j][2] >= 0) and (matrix_rgb[i][j][2] < 0.2):
    #             h[11] += 1
    #         elif (matrix_rgb[i][j][2] >= 0.2) and (matrix_rgb[i][j][2] < 0.7):
    #             h[12] += 1
    #         elif (matrix_rgb[i][j][2] >= 0.7) and (matrix_rgb[i][j][2] <= 1):
    #             h[13] += 1

    # return h

def main():
    start = time.time()
    path_foto = r"C:\Users\ACER\Documents\GitHub\Algeo02-22032\src\example\logic\skulll.jpg"
    hehe = convert_rgb_hsv(path_foto)
    print(hehe)

    path_fot = r"C:\Users\ACER\Documents\GitHub\Algeo02-22032\src\example\logic\skulll.jpg"
    heh = convert_rgb_hsv(path_fot)
    print(heh)
    end = time.time()

    similar = cosine(hehe,heh)
    print(similar, "%")
    print("time :" , end-start, "s")
if __name__ == "__main__":
    main()