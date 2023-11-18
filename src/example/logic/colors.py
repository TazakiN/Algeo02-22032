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
    
    # membuat histogram
    bins_h = [1, 26, 41, 121, 191, 271, 295, 316, 360] 
    bins_s = [0, 0.2, 0.7, 1] 
    bins_v = [0, 0.2, 0.7, 1] 

    hist_h, bin_edges = np.histogram(h,bins_h)
    hist_s, bin_edges = np.histogram(s,bins_s)
    hist_v, bin_edges = np.histogram(v,bins_v)

    hsv = np.concatenate((hist_h, hist_s, hist_v))

    return hsv



start = time.time()
path_foto = r"C:\Users\ACER\Documents\GitHub\Algeo02-22032\src\example\logic\macan.jpg"
hehe = convert_rgb_hsv(path_foto)

path_fot = r"C:\Users\ACER\Documents\GitHub\Algeo02-22032\src\example\logic\maung.jpg"
heh = convert_rgb_hsv(path_fot)

end = time.time()

similar = cosine(hehe,heh)
print(similar, "%")
print("time :" , end-start, "s")
    
