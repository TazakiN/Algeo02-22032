from django.shortcuts import render
from django.http import JsonResponse
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import logging
from example.models import Image, Dataset
import urllib.parse


logger = logging.getLogger(__name__)
method = "color"


# tampilan utama
class MainView(TemplateView):
    template_name = "example/main.html"


def aboutUs(request):
    return render(request, "example/about-us.html")


def explanation(request):
    return render(request, "example/explanation.html")


def upload(request):
    if request.method == "POST":
        image = request.FILES.get("file")
        if image:
            # Gunakan FileSystemStorage untuk menyimpan file secara otomatis
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "images"))
            filename = fs.save(image.name, image)
            image_url = fs.url(filename)

            # Buat instance model Image dan simpan ke database
            image_model = Image(name=image.name, image=image_url)
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

            # Buat instance model Dataset dan simpan ke database
            dataset_model = Dataset(name=image.name, image=image_url)
            dataset_model.save()

            # Respon sukses
            return JsonResponse({"message": "Dataset berhasil diunggah"})

    # Respon gagal
    return JsonResponse({"message": "Gagal mengunggah dataset"})


@csrf_exempt
def process_button(request):
    if request.method == "POST":
        dataset_path = "media/dataset/"
        image_files = [
            os.path.join(dataset_path, f)
            for f in os.listdir(dataset_path)
            if os.path.isfile(os.path.join(dataset_path, f))
        ]

        # Mengembalikan JsonResponse dengan file gambar
        return JsonResponse({"image_files": image_files})


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


@csrf_exempt
def process_image(request):
    if request.method == "POST":
        cbir_method = request.POST.get("cbir_method_hidden")

        # bagian pemilihan metode CBIR
        if cbir_method == "color":
            logger.info("Color method selected")  # ntar diganti
        elif cbir_method == "texture":
            logger.info("Texture method selected")  # ntar diganti
        else:
            logger.error("Unrecognized method: %s", cbir_method)

        return HttpResponse()
    else:
        return HttpResponse()


def update_result(request):
    # Ambil semua objek Dataset dari database
    datasets = Dataset.objects.all()

    # Buat daftar dictionary dengan URL dan nama gambar
    data = [
        {
            "image_url": "/".join(
                ["media", "dataset", os.path.basename(str(dataset.image))]
            ),
            "image_name": urllib.parse.unquote(os.path.basename(str(dataset.image))),
        }
        for dataset in datasets
    ]

    # Buat objek Paginator
    paginator = Paginator(data, 15)  # Tampilin 15 gambar per halaman

    # Dapatkan halaman yang diminta oleh pengguna
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Kirim respons JSON dengan data dan informasi paginasi
    return JsonResponse(
        {
            "data": page_obj.object_list,
            "has_previous": page_obj.has_previous(),
            "has_next": page_obj.has_next(),
            "current_page": page_obj.number,
            "total_pages": paginator.num_pages,
        }
    )
