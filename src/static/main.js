document.addEventListener("DOMContentLoaded", function () {
  const methodCheckbox = document.getElementById("methodCheckbox");
  const cbirMethodHidden = document.getElementById("cbirMethodHidden");
  const methodSwitch = document.querySelector(".method-switch");
  const url = methodSwitch.getAttribute("data-url");
  const csrfToken = methodSwitch.getAttribute("data-csrf");

  methodCheckbox.addEventListener("change", function () {
    if (methodCheckbox.checked) {
      cbirMethodHidden.value = "texture";
    } else {
      cbirMethodHidden.value = "color";
    }

    // Mengirim POST request dengan AJAX
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.setRequestHeader("X-CSRFToken", csrfToken);
    xhr.send(
      "cbir_method_hidden=" + encodeURIComponent(cbirMethodHidden.value)
    );
  });
});

Dropzone.options.myAwesomeDropzone = {
  maxFiles: 1,
  acceptedFiles: "image/*",
  init: function () {
    this.on("addedfile", function (file) {
      if (this.files[1] != null) {
        this.removeFile(this.files[0]);
      }

      // Menghapus gambar dan nama file sebelumnya
      var imagePreview = document.getElementById("imagePreview");
      while (imagePreview.firstChild) {
        imagePreview.removeChild(imagePreview.firstChild);
      }

      // nampilin gambar
      var reader = new FileReader();
      reader.onload = function (e) {
        var img = document.createElement("img");
        img.src = e.target.result;
        img.style.width = "200px";
        imagePreview.appendChild(img);

        var filename = document.createElement("p");
        filename.textContent = file.name;
        imagePreview.appendChild(filename);
      };
      reader.readAsDataURL(file);

      // Menyembunyikan Dropzone setelah file diupload
      document.getElementById("my-awesome-dropzone").style.opacity = "0";
      document.getElementById("my-awesome-dropzone").style.position =
        "absolute";
    });
  },
};

Dropzone.options.myAwesomeDropzoneDataset = {
  acceptedFiles: "image/*",
  init: function () {
    var uploadMessage;
    var uploadInterval;

    this.on("addedfile", function (file) {
      var datasetPreview = document.getElementById("datasetPreview");
      while (datasetPreview.firstChild) {
        datasetPreview.removeChild(datasetPreview.firstChild);
      }

      var foldername = document.createElement("p");
      foldername.textContent = file.name;
      datasetPreview.appendChild(foldername);

      document.getElementById("my-awesome-dropzone-dataset").style.opacity =
        "0";
      document.getElementById("my-awesome-dropzone-dataset").style.position =
        "absolute";

      uploadMessage = document.createElement("p");
      uploadMessage.textContent = "Sedang mengunggah: " + file.name;
      datasetPreview.appendChild(uploadMessage);

      var dotCount = 0;
      uploadInterval = setInterval(function () {
        dotCount = (dotCount + 1) % 4;
        var dots = new Array(dotCount + 1).join(".");
        uploadMessage.textContent = "Sedang mengunggah: " + file.name + dots;
      }, 1000);
    });

    this.on("complete", function (file) {
      if (
        this.getUploadingFiles().length === 0 &&
        this.getQueuedFiles().length === 0
      ) {
        clearInterval(uploadInterval);

        uploadMessage.parentNode.removeChild(uploadMessage);

        var datasetPreview = document.getElementById("datasetPreview");
        var successMessage = document.createElement("p");
        successMessage.textContent = "Dataset berhasil diunggah!";
        datasetPreview.appendChild(successMessage);
      }
    });
  },
};

var page = 1; // halaman yang pertama ditampilkan

function updateImages() {
  $.ajax({
    url: $("#processForm").data("url") + "?page=" + page,
    type: "POST",
    data: new FormData($("#processForm")[0]),
    contentType: false,
    cache: false,
    processData: false,
    success: function (data) {
      console.log(data);
      if (data && data.data) {
        var html = "";
        data.data.forEach(function (item) {
          html +=
            '<div class="image-container"> <img src="' +
            item.image_url +
            '" alt="' +
            item.image_name +
            '" /> <div class="image-name">' +
            item.image_name +
            '</div> <div class="image-similarity">' +
            item.similarity.toFixed(10) +
            "% similarity</div> </div>";
        });

        $("#result-image").html(html);

        // Buat HTML untuk paginasi
        var paginationHtml = '<div class="pagination">';

        if (data.has_previous) {
          paginationHtml += '<button id="previous-button">Previous</button>';
        }

        paginationHtml +=
          "<span id='page-info'>Page " +
          data.current_page +
          " of " +
          data.total_pages +
          "</span>";

        // Jika ada halaman berikutnya, tampilkan tombol "Next"
        if (data.has_next) {
          paginationHtml += '<button id="next-button">Next</button>';
        }

        paginationHtml += "</div>";

        // Sisipkan HTML paginasi ke dalam elemen yang sesuai di halaman Anda
        $("#pagination").html(paginationHtml);

        // Tambahkan event listener untuk tombol "Previous" dan "Next"
        $("#previous-button").click(function () {
          page--;
          updateImages();
        });
        $("#next-button").click(function () {
          page++;
          updateImages();
        });

        // Tampilkan jumlah gambar yang ditemukan dan waktu proses CBIR
        $(".result-title").html(
          "Result: " +
            data.num_images +
            " images found in " +
            data.time_taken.toFixed(5) +
            " seconds"
        );
      } else {
        alert("Gagal memproses permintaan.");
      }
    },
  });
}

$(document).ready(function () {
  $("#processButton").click(function () {
    page = 1; // Mulai dari halaman pertama saat tombol diproses diklik
    updateImages();
  });
});
