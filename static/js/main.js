// Wait for DOM to load
document.addEventListener("DOMContentLoaded", function () {
    // ===== Page Load Animation =====
    document.body.classList.add("animate__animated", "animate__fadeIn");

    // ===== File Input Preview on Upload Page =====
    const fileInput = document.getElementById('logFile');
    const fileNameDisplay = document.getElementById('fileNameDisplay');

    if (fileInput && fileNameDisplay) {
        fileInput.addEventListener('change', function () {
            const fileName = this.files[0] ? this.files[0].name : "No file chosen";
            fileNameDisplay.textContent = fileName;
        });
    }

    // ===== Optional: Toast Notification (Success/Error Upload) =====
    const toastTrigger = document.getElementById('uploadToastTrigger');
    const toastElement = document.getElementById('uploadToast');
    if (toastTrigger && toastElement) {
        const toast = new bootstrap.Toast(toastElement);
        toastTrigger.addEventListener('click', () => {
            toast.show();
        });
    }

    // ===== Optional: Table Sorting Logic for Explorer Page =====
    const tables = document.querySelectorAll("table.sortable");
    tables.forEach((table) => {
        table.querySelectorAll("th").forEach((header, index) => {
            header.style.cursor = "pointer";
            header.addEventListener("click", () => {
                sortTableByColumn(table, index);
            });
        });
    });

    // ===== Sidebar toggle logic (for mobile, future enhancement) =====
    const sidebarToggle = document.getElementById("sidebarToggle");
    if (sidebarToggle) {
        sidebarToggle.addEventListener("click", () => {
            document.querySelector(".sidebar").classList.toggle("d-none");
        });
    }
});

// ========== Utility: Table Sort ==========
function sortTableByColumn(table, columnIndex) {
    const rows = Array.from(table.querySelectorAll("tbody tr"));
    const isAsc = table.dataset.sortOrder !== "asc";
    rows.sort((rowA, rowB) => {
        const cellA = rowA.children[columnIndex].innerText.toLowerCase();
        const cellB = rowB.children[columnIndex].innerText.toLowerCase();
        return isAsc ? cellA.localeCompare(cellB) : cellB.localeCompare(cellA);
    });

    table.dataset.sortOrder = isAsc ? "asc" : "desc";
    const tbody = table.querySelector("tbody");
    rows.forEach(row => tbody.appendChild(row));
}
