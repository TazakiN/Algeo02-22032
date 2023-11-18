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


# gambar -> matrix rgb 3d -> array h ada array s ada array v -> gw hitung histogram di array hsv -> dioutput terus cosine


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

    # Stack H, S, V to get the HSV image
    # hsv_image = np.stack((h, s, v), axis=-1)

    # Merupakan array untuk menyimpan histogram hsv yang kemudian dicosine
    hsv = np.zeros(14)

    # membuat histogram
    for i in range(len(h)):
        for j in range(len(h[i])):
            if (h[i][j] >= 316) and (h[i][j] <= 360):
                hsv[0] += 1
            elif (h[i][j] >= 1) and (h[i][j] <= 25):
                hsv[1] += 1
            elif (h[i][j] >= 26) and (h[i][j] <= 40):
                hsv[2] += 1
            elif (h[i][j] >= 41) and (h[i][j] <= 120):
                hsv[3] += 1
            elif (h[i][j] >= 121) and (h[i][j] <= 190):
                hsv[4] += 1
            elif (h[i][j] >= 191) and (h[i][j] <= 270):
                hsv[5] += 1
            elif (h[i][j] >= 271) and (h[i][j] <= 295):
                hsv[6] += 1
            elif (h[i][j] >= 295) and (h[i][j] <= 315):
                hsv[7] += 1

            if (s[i][j] >= 0) and (s[i][j] < 0.2):
                hsv[8] += 1
            elif (s[i][j] >= 0.2) and (s[i][j] < 0.7):
                hsv[9] += 1
            elif (s[i][j] >= 0.7) and (s[i][j] <= 1):
                hsv[10] += 1

            if (v[i][j] >= 0) and (v[i][j] < 0.2):
                hsv[11] += 1
            elif (v[i][j] >= 0.2) and (v[i][j] < 0.7):
                hsv[12] += 1
            elif (v[i][j] >= 0.7) and (v[i][j] <= 1):
                hsv[13] += 1

    return hsv


# def main():
#     start = time.time()
#     path_foto = (
#         r"C:\Users\ACER\Documents\GitHub\Algeo02-22032\src\example\logic\skulll.jpg"
#     )
#     hehe = convert_rgb_hsv(path_foto)

#     path_fot = (
#         r"C:\Users\ACER\Documents\GitHub\Algeo02-22032\src\example\logic\skulll.jpg"
#     )
#     heh = convert_rgb_hsv(path_fot)

#     end = time.time()

#     similar = cosine(hehe, heh)
#     print(similar, "%")
#     print("time :", end - start, "s")


# if __name__ == "__main__":
#     main()
