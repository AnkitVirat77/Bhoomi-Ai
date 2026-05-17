function uploadImage() {
    const fileInput = document.getElementById("imageInput");
    const file = fileInput.files[0];
  
    if (!file) {
      alert("Please upload an image");
      return;
    }
  
    // Preview image
    const preview = document.getElementById("preview");
    preview.src = URL.createObjectURL(file);
  
    const formData = new FormData();
    formData.append("file", file);
  
    fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      body: formData
    })
    .then(res => res.json())
    .then(data => {
      document.getElementById("result").innerHTML = `
        <p><b>Disease:</b> ${data.disease}</p>
        <p><b>Confidence:</b> ${data.confidence}</p>
        <p><b>Solution:</b> ${data.solution}</p>
      `;
    })
    .catch(err => console.error(err));
  }