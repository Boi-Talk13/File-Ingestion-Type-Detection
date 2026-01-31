document.addEventListener("DOMContentLoaded", () => {

    const dropZone = document.getElementById("dropZone");
    const fileInput = document.getElementById("fileInput");
    const selectBtn = document.getElementById("selectBtn");
    const uploadBtn = document.getElementById("uploadBtn");
    const result = document.getElementById("result");
    const fileCount = document.getElementById("fileCount");

    let selectedFiles = [];

    /* HARD CHECK */
    if (!dropZone || !fileInput || !selectBtn || !uploadBtn || !fileCount) {
        console.error("Missing required HTML elements");
        return;
    }

    /* SELECT FILES */
    selectBtn.addEventListener("click", () => {
        fileInput.click();
    });

    fileInput.addEventListener("change", () => {
        selectedFiles = Array.from(fileInput.files);

        fileCount.textContent = selectedFiles.length
            ? `${selectedFiles.length} file(s) selected`
            : "";

        uploadBtn.disabled = selectedFiles.length === 0;
    });

    /* DRAG & DROP */
    dropZone.addEventListener("dragover", e => {
        e.preventDefault();
        dropZone.classList.add("dragover");
    });

    dropZone.addEventListener("dragleave", () => {
        dropZone.classList.remove("dragover");
    });

    dropZone.addEventListener("drop", e => {
        e.preventDefault();
        dropZone.classList.remove("dragover");

        selectedFiles = Array.from(e.dataTransfer.files);

        const dt = new DataTransfer();
        selectedFiles.forEach(f => dt.items.add(f));
        fileInput.files = dt.files;

        fileCount.textContent = `${selectedFiles.length} file(s) selected`;
        uploadBtn.disabled = selectedFiles.length === 0;
    });

    /* UPLOAD */
    uploadBtn.addEventListener("click", async () => {
        if (!selectedFiles.length) return;

        const formData = new FormData();
        selectedFiles.forEach(f => formData.append("files", f));

        result.textContent = "Uploading...\n\n";

        try {
            const res = await fetch("/upload", {
                method: "POST",
                body: formData
            });

            const data = await res.json();
            result.textContent = "";

            data.forEach(file => {
                result.textContent += formatFile(file);
            });

        } catch (err) {
            console.error(err);
            result.textContent = "Upload failed";
        }
    });

    function formatFile(f) {
        return `
--------------------------------
File Name   : ${f.file_name}
File Type   : ${f.file_type?.toUpperCase()}
Size (KB)   : ${f.size_kb}
Hash        : ${f.hash}
Status      : ${f.status}
Mime Type   : ${f.mime_type}
Uploaded At : ${f.uploaded_at}
Duplicate   : ${f.duplicate}
Scan Status : ${f.scan_status}
`;
    }
});