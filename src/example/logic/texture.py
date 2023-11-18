from PIL import Image
import numpy as np
import time

# def ImagetoRGB (path) : # input merupakan alamat atau path dari image
#     image = Image.open(path)
#     image_array = image.convert("RGB")
#     image_array = np.array(image_array)
#     return image_array


# def grayscale(data) : # input merupakan matriks RGB
#     baris = len(data)
#     kolom = len(data[0])
#     dataGray =[[0 for i in range(kolom)] for j in range(baris)]
#     for i in range (baris) :
#         for j in range (kolom) :
#             rgb = data[i][j]
#             dataGray[i][j] = round((rgb[0] * 0.29) + (rgb[1] * 0.587) + (rgb[2] * 0.114))
#     return dataGray

def CoccurenceMatrix (data) : # input merupakan matriks grayscale
    baris = len(data)       # menggunakan distance 1 angle 0 degree
    kolom = len(data[0])
    Matrix = np.zeros((256, 256))

    for i in range(baris) :
        for j in range(kolom-1) :
            x = int(data[i][j])
            y = int(data[i][j+1])

            Matrix[x][y] += 1
    return Matrix

def symmetric (data) : # input merupakan kookuren
    transpose = np.transpose(data)
    transpose = np.add(data,transpose)
    return transpose

def normalize (data) : # input merupakan simetri
    data = np.divide(data, np.sum(data))
    return data

def contrast (data) : # input merupakan matriks symmetric
    array_index = np.arange(data.shape[0])
    m_square = np.square(array_index[:, None] - array_index)

    kontras = np.sum(m_square * data)
    return kontras 
    # kontras = 0
    # for i in range(len(data)) :
    #     for j in range(len(data[0])) :
    #         kontras += data[i][j] * pow(i - j, 2)
    # return kontras

def homogeneity (data) : # input merupakan matriks symmetric
    homo = 0 
    for i in range(len(data)) :
        for j in range(len(data[0])) :
            homo += data[i][j] / (1 + pow(i - j, 2))
    return homo

def entropy (data) : # input merupakan matriks symmetric
    result = 0 
    for i in range(len(data)) :
        for j in range(len(data[0])) :
            if (data[i][j] != 0) :
                result += data[i][j] * np.log10(data[i][j])
    return result

def dissimilarity (data) : # input merupakan matriks symmetric
    result = 0 
    for i in range(len(data)) :
        for j in range(len(data[0])) :
            result += data[i][j] * abs(i - j)
    return result


def cosine (A, B) :
    return (np.dot(A,B)/(np.linalg.norm(A)*np.linalg.norm(B))) * 100
    # dot = 0
    # panjangA = 0 
    # panjangB = 0 
    # for i in range(len(A)) :
    #     dot += (A[i] * B[i]) 
    #     panjangA += pow(A[i], 2)
    #     panjangB += pow(B[i], 2)
    # panjangA = np.sqrt(panjangA)
    # panjangB = np.sqrt(panjangB)
    # similarity = (dot / (panjangA * panjangB))* 100
    # return similarity

def normVektor (vektor) :
    total = 0 
    for i in range(len(vektor)) :
        total += vektor[i]
    for i in range(len(vektor)) :
        vektor[i] = vektor[i] / total
    return vektor

def getData (path) : # return vektor
    # ngambil RGB
    image = Image.open(path)
    image_array = image.convert("RGB")
    image_array = np.array(image_array)

    # ngubah grayscale
    data = np.dot(image_array[..., :3], [0.299, 0.587, 0.114])

    data = CoccurenceMatrix(data)
    data = symmetric(data)
    data = normalize(data)

    array_index = np.arange(data.shape[0])
    m_square = np.square(array_index[:, None] - array_index)

    kontras = np.sum(data * m_square)
    homo = np.sum(data / (m_square+1))
    entro = np.sum(np.where(data > 0, data * np.log2(data + 1e-10), 0))
    energy = np.sum(data**2)

    mean = np.mean(array_index)
    m_mean = (array_index[:, None]-mean) * (array_index-mean)
    std = np.std(array_index)
    correlation = np.sum((data*m_mean) / std**2)


    # kontras = contrast(data) 
    # homo = homogeneity(data)
    # entro = entropy(data)
    # for i in range(len(data)) :
    #     for j in range(len(data[0])) :
    #         kontras += data[i][j] * pow(i - j, 2)
    #         homo += data[i][j] / (1 + pow(i - j, 2))
    #         if (data[i][j] != 0) :
    #             entro += data[i][j] * np.log10(data[i][j])

    vektor = [kontras, homo, -entro, energy, correlation]
    return vektor

# start = time.time()
# kucingpaw = getData("0.jpg")
# kucingchill = getData("1.jpg")
# similarity = cosine(kucingpaw, kucingchill)
# end = time.time()

# print("kontras:" , kucingpaw[0] , "Homo:", kucingpaw[1], "entro:" , kucingpaw[2])
# print("kontras:" , kucingchill[0] , "Homo:", kucingchill[1], "entro:" , kucingchill[2])
# print(similarity, "%")
# print("time:", (end - start) * 1000 , "ms")
