import os
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import logging
from example.models import Image, Dataset
import urllib.parse
from example.logic.texture import *


logger = logging.getLogger(__name__)
method = "color"

# variabel data
imageDataTexture = None
imageDataColor = None
datasetImageDataTexture = []
datasetImageDataColor = []


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

    if request.method == "POST":
        image = request.FILES.get("file")
        if image:
            # Gunakan FileSystemStorage untuk menyimpan file secara otomatis
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "images"))
            filename = fs.save(image.name, image)
            image_url = fs.url(filename)

            # Simpan path dari gambar yang di-upload
            uploaded_image_path = os.path.join(settings.MEDIA_ROOT, "images", filename)

            # Panggil fungsi getData untuk mendapatkan data dari gambar yang di-upload
            imageDataTexture = getData(uploaded_image_path)

            # Buat instance model Image dan simpan ke database
            image_model = Image(name=image.name, image=image_url)
            image_model.save()

            # respon sukses
            return JsonResponse({"message": "Gambar berhasil diunggah"})

    # Respon gagal
    return JsonResponse({"message": "Gagal mengunggah gambar"})


def uploadDataset(request):
    global datasetImageDataTexture
    global datasetImageDataColor

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
            image_data = getData(uploaded_image_path)

            # Tambahkan hasil getData dari gambar ke dalam list datasetImageDataGray
            datasetImageDataTexture.append(image_data)

            # Buat instance model Dataset dan simpan ke database
            dataset_model = Dataset(name=image.name, image=image_url)
            dataset_model.save()

            # Respon sukses
            return JsonResponse({"message": "Dataset berhasil diunggah"})

    # Respon gagal
    return JsonResponse({"message": "Gagal mengunggah dataset"})


def methodCBIR(request):
    if request.method == "POST":
        cbir_method = request.POST.get("cbir_method_hidden")
        if cbir_method == "color":
            logger.info("Color method selected")
        elif cbir_method == "texture":
            logger.info("Texture method selected")
        else:
            logger.error("Unrecognized method: %s", cbir_method)

    # Handle GET request or other cases
    return HttpResponse()


def update_result(request):
    global imageDataTexture
    global datasetImageDataTexture

    if imageDataTexture is None:
        return JsonResponse({"error": "No uploaded image for comparison"})

    similar_images = []
    similarity_threshold = 60

    for idx, dataset_image in enumerate(datasetImageDataTexture):
        similarity = cosine(imageDataTexture, dataset_image)
        if similarity > similarity_threshold:
            dataset_image_info = Dataset.objects.all()[idx]
            similar_images.append(
                {
                    "image_url": "/".join(
                        [
                            "media",
                            "dataset",
                            os.path.basename(str(dataset_image_info.image)),
                        ]
                    ),
                    "image_name": urllib.parse.unquote(
                        os.path.basename(str(dataset_image_info.image))
                    ),
                    "similarity": similarity,
                }
            )

    # Sorting based on similarity in descending order
    similar_images.sort(key=lambda x: x["similarity"], reverse=True)

    # Pagination
    paginator = Paginator(similar_images, 6)  # Tampilkan 6 gambar per halaman
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return JsonResponse(
        {
            "data": list(page_obj.object_list),
            "has_previous": page_obj.has_previous(),
            "has_next": page_obj.has_next(),
            "current_page": page_obj.number,
            "total_pages": paginator.num_pages,
        }
    )
