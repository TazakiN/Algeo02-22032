from PIL import Image
import numpy as np

# Urutan Pemrosesan
# Gambar -> matrix rgb 3d -> array h ada array s ada array v -> gw hitung histogram di array hsv -> dioutput terus cosine


def ImagetoRGB(path):  # input merupakan alamat atau path dari image
    image = Image.open(path)
    image_array = image.convert("RGB")
    image_array = np.array(image_array)
    return image_array


def cosine(A, B):
    return (np.dot(A, B) / (np.linalg.norm(A) * np.linalg.norm(B))) * 100


def convert_rgb_hsv(path_gambar):
    # Fungsi di bawah mengubah gambar menjadi matrix rgb
    matrix_rgb = ImagetoRGB(path_gambar)

    # Normalisasi rgb
    matrix_rgb = matrix_rgb / 255.0

    # Memisahkan r, g, dan b
    r, g, b = matrix_rgb[:, :, 0], matrix_rgb[:, :, 1], matrix_rgb[:, :, 2]

    # Merupakan array v dari seluruh pixel (cmax)
    v = np.max(matrix_rgb, axis=2)

    delta = v - np.min(matrix_rgb, axis=2)

    # Merupakan array s dari seluruh pixel
    s = np.where(v != 0, delta / v, 0)

    # Merupakan array h dari seluruh pixel
    h = np.where(
        (delta != 0),
        (
            np.where(
                (v == r),
                60 * ((g - b) / (delta + 1e-10) % 6),
                np.where(
                    (v == g),
                    60 * ((b - r) / (delta + 1e-10) + 2),
                    60 * ((r - g) / (delta + 1e-10) + 4),
                ),
            )
        ),
        0,
    )

    # Adjust hue values to be in the range [0, 360) #anjim waktunya 0.03
    h = (h + 360) % 360

    # membuat histogram
    bins_h = [1, 26, 41, 121, 191, 271, 295, 316, 360]
    bins_s = [0, 0.2, 0.7, 1]
    bins_v = [0, 0.2, 0.7, 1]

    hist_h, bin_edges = np.histogram(h, bins_h)
    hist_s, bin_edges = np.histogram(s, bins_s)
    hist_v, bin_edges = np.histogram(v, bins_v)

    hsv = np.concatenate((hist_h, hist_s, hist_v))

    # Kode Tanpa Bantuan Numpy:

    # Inisialisasi vektor pernyimpanan histogram
    # hsv = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # 8 elemen pertama adalah histogram h
    # 3 elemen selanjutnya adalah histogram s
    # 3 elemen terakhir adalah histogram v
    
    # Normalisasi
    # matrix_rgb = matrix_rgb/255.0
    
    # Iterasi seluruh elemen matrix dan mengubahnya menjadi hsv
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

    #         Mengisi nilai h
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

    #         Mengisi nilai s        
    #         if cmax == 0:
    #             matrix_rgb[i][j][1] = 0
    #         else:
    #             matrix_rgb[i][j][1] = delta / cmax

    #         Mengisi nilai v
    #         matrix_rgb[i][j][2] = cmax

    #         Mengisi histogram hsv
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

    return hsv