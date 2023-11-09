from email.policy import HTTP
from django.shortcuts import render
from django.http import JsonResponse
import os
from django.conf import settings
from .forms import CBIRMethodForm
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import logging


logger = logging.getLogger(__name__)


class MainView(TemplateView):
    template_name = "docs/main.html"


def upload(request):
    if request.method == "POST":
        image = request.FILES.get("file")
        if image:
            # Simpan gambar ke direktori MEDIA_ROOT
            with open(
                os.path.join(settings.MEDIA_ROOT, image.name), "wb+"
            ) as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            # Respon sukses (atau sesuaikan dengan kebutuhan Anda)
            return JsonResponse({"message": "Gambar berhasil diunggah"})

    # Respon gagal jika tidak ada gambar atau kesalahan lainnya
    return JsonResponse({"message": "Gagal mengunggah gambar"})


def methodCBIR(request):
    if request.method == "POST":
        cbir_method = request.POST.get("cbir_method_hidden")
        if cbir_method == "color":
            # Log a message to the console
            logger.info("Color method selected")
        elif cbir_method == "texture":
            # Log a message to the console
            logger.info("Texture method selected")
        else:
            # Handle the case where the value is not recognized
            logger.error("Unrecognized method: %s", cbir_method)

    # Handle GET request or other cases
    return HttpResponse()


@csrf_exempt
def process_image(request):
    if request.method == "POST":
        # Tempatkan fungsi Python Anda di sini
        return HttpResponse("Fungsi Python telah dieksekusi!")
    else:
        return HttpResponse("Halaman ini memerlukan POST request.")
