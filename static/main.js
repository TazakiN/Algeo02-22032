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

      // Membuat elemen baru untuk menampilkan gambar
      var reader = new FileReader();
      reader.onload = function (e) {
        var img = document.createElement("img");
        img.src = e.target.result;
        img.style.width = "200px"; // Atur lebar gambar sesuai keinginan Anda
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
