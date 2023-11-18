import os
from django.utils import timezone
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.core.paginator import Paginator
from example.models import ImageQuery, Dataset
from example.logic.texture import *
from example.logic.colors import *
import urllib.parse
import logging


logger = logging.getLogger(__name__)
method = "color"
time_taken = 0

# variabel data
imageDataTexture = None
imageDataColor = None


# tampilan utama
class MainView(TemplateView):
    template_name = "example/main.html"


def aboutUs(request):
    return render(request, "example/about-us.html")


def explanation(request):
    return render(request, "example/explanation.html")


def upload(request):
    global imageDataTexture
    global imageDataColor
    global time_taken

    if request.method == "POST":
        image = request.FILES.get("file")
        time_taken = 0
        if image:
            # Gunakan FileSystemStorage untuk menyimpan file secara otomatis
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "images"))
            filename = fs.save(image.name, image)
            image_url = fs.url(filename)

            # Simpan path dari gambar yang di-upload
            uploaded_image_path = os.path.join(settings.MEDIA_ROOT, "images", filename)

            # Panggil fungsi getData untuk mendapatkan data dari gambar yang di-upload
            imageDataTexture = getData(uploaded_image_path)
            imageDataColor = convert_rgb_hsv(uploaded_image_path)

            # Buat instance model Image dan simpan ke database
            image_model = ImageQuery(name=image.name, image=image_url)
            image_model.save()

            # respon sukses
            return JsonResponse({"message": "Gambar berhasil diunggah"})

    # Respon gagal
    return JsonResponse({"message": "Gagal mengunggah gambar"})


def uploadDataset(request):
    if request.method == "POST":
        image = request.FILES.get("file")
        if image:
            # Gunakan FileSystemStorage untuk menyimpan file secara otomatis
            fs = FileSystemStorage(
                location=os.path.join(settings.MEDIA_ROOT, "dataset")
            )
            filename = fs.save(image.name, image)
            image_url = fs.url(filename)

            # Simpan path dari gambar yang di-upload
            uploaded_image_path = os.path.join(settings.MEDIA_ROOT, "dataset", filename)

            # Panggil fungsi getData untuk mendapatkan data dari gambar yang di-upload
            image_data_texture = getData(uploaded_image_path)
            image_data_color = convert_rgb_hsv(uploaded_image_path)

            # Buat instance model Dataset dan simpan ke database
            dataset_model = Dataset(
                name=image.name,
                image=image_url,
                contrast=image_data_texture[0],
                homogeneity=image_data_texture[1],
                entropy=image_data_texture[2],
                energy=image_data_texture[3],
                correlation=image_data_texture[4],
                h0=image_data_color[0],
                h1=image_data_color[1],
                h2=image_data_color[2],
                h3=image_data_color[3],
                h4=image_data_color[4],
                h5=image_data_color[5],
                h6=image_data_color[6],
                h7=image_data_color[7],
                s0=image_data_color[8],
                s1=image_data_color[9],
                s2=image_data_color[10],
                v0=image_data_color[11],
                v1=image_data_color[12],
                v2=image_data_color[13],
            )
            dataset_model.save()

            # Respon sukses
            return JsonResponse({"message": "Dataset berhasil diunggah"})

    # Respon gagal
    return JsonResponse({"message": "Gagal mengunggah dataset"})


def methodCBIR(request):
    global method
    global time_taken

    if request.method == "POST":
        cbir_method = request.POST.get("cbir_method_hidden")
        if cbir_method == "color":
            logger.info("Color method selected")
            method = "color"
        elif cbir_method == "texture":
            logger.info("Texture method selected")
            method = "texture"
        else:
            logger.error("Unrecognized method: %s", cbir_method)
    time_taken = 0
    return HttpResponse()


def update_result(request):
    global imageDataTexture
    global imageDataColor
    global time_taken
    global method

    if imageDataTexture is None:
        return JsonResponse({"error": "No uploaded image for comparison"})

    # hitung waktu kalo waktu belum pernah dihitung
    if time_taken == 0:
        start_time = timezone.now()

    similar_images = []
    similarity_threshold = 60

    # ambil semua objek Dataset dari database
    dataset_images = Dataset.objects.all()

    if method == "texture":
        for dataset_image in dataset_images:
            # ambil data dari model Dataset
            contrast = dataset_image.contrast
            homogeneity = dataset_image.homogeneity
            entropy = dataset_image.entropy
            energy = dataset_image.energy
            correlation = dataset_image.correlation

            # buat list data dari model Dataset
            dataset_image_data = [contrast, homogeneity, entropy, energy, correlation]

            # hitung similarity
            similarity = cosine(imageDataTexture, dataset_image_data)

            if similarity > similarity_threshold:
                similar_images.append(
                    {
                        "image_url": "/".join(
                            [
                                "media",
                                "dataset",
                                os.path.basename(str(dataset_image.image)),
                            ]
                        ),
                        "image_name": urllib.parse.unquote(
                            os.path.basename(str(dataset_image.image))
                        ),
                        "similarity": similarity,
                    }
                )

        # sorting berdasarkan similarity
        similar_images.sort(key=lambda x: x["similarity"], reverse=True)
    else:
        for dataset_image in dataset_images:
            # ambil data dari model Dataset
            h0 = dataset_image.h0
            h1 = dataset_image.h1
            h2 = dataset_image.h2
            h3 = dataset_image.h3
            h4 = dataset_image.h4
            h5 = dataset_image.h5
            h6 = dataset_image.h6
            h7 = dataset_image.h7
            s0 = dataset_image.s0
            s1 = dataset_image.s1
            s2 = dataset_image.s2
            v0 = dataset_image.v0
            v1 = dataset_image.v1
            v2 = dataset_image.v2

            # buat list data dari model Dataset
            dataset_image_data = [
                h0,
                h1,
                h2,
                h3,
                h4,
                h5,
                h6,
                h7,
                s0,
                s1,
                s2,
                v0,
                v1,
                v2,
            ]

            # hitung similarity
            similarity = cosine(imageDataColor, dataset_image_data)

            if similarity > similarity_threshold:
                similar_images.append(
                    {
                        "image_url": "/".join(
                            [
                                "media",
                                "dataset",
                                os.path.basename(str(dataset_image.image)),
                            ]
                        ),
                        "image_name": urllib.parse.unquote(
                            os.path.basename(str(dataset_image.image))
                        ),
                        "similarity": similarity,
                    }
                )

        # sorting berdasarkan similarity
        similar_images.sort(key=lambda x: x["similarity"], reverse=True)

    # Pagination
    paginator = Paginator(similar_images, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if time_taken == 0:
        end_time = timezone.now()
        time_taken = (end_time - start_time).total_seconds()

    return JsonResponse(
        {
            "data": list(page_obj.object_list),
            "has_previous": page_obj.has_previous(),
            "has_next": page_obj.has_next(),
            "current_page": page_obj.number,
            "total_pages": paginator.num_pages,
            "num_images": len(similar_images),
            "time_taken": time_taken,
        }
    )
