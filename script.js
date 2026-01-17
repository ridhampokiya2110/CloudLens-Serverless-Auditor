// REPLACE THIS URL AFTER STEP 3 IN THE GUIDE BELOW
const API_ENDPOINT = "https://0a7bnxdqx6.execute-api.ap-south-1.amazonaws.com/";

// Function 1: Upload File (Converts to Base64 and sends to API)
async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const status = document.getElementById('uploadStatus');
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a file!");
        return;
    }

    status.innerText = "Uploading...";

    // Convert file to Base64
    const reader = new FileReader();
    reader.onload = async function(e) {
        const base64Data = e.target.result.split(',')[1]; // Remove header

        try {
            const response = await fetch(API_ENDPOINT, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    filename: file.name,
                    fileContent: base64Data
                })
            });

            if (response.ok) {
                status.innerText = "✅ Upload Successful! Check email.";
                setTimeout(fetchLogs, 2000); // Refresh table
            } else {
                status.innerText = "❌ Upload Failed.";
            }
        } catch (error) {
            console.error(error);
            status.innerText = "❌ Error connecting to server.";
        }
    };
    reader.readAsDataURL(file);
}

// Function 2: Fetch Data from DynamoDB
async function fetchLogs() {
    try {
        const response = await fetch(API_ENDPOINT);
        const data = await response.json();
        
        const tableBody = document.getElementById('logTableBody');
        tableBody.innerHTML = ""; // Clear existing data

        data.forEach(item => {
            const row = `<tr>
                <td>${item.filename}</td>
                <td>${item.ai_labels || "Processing..."}</td>
                <td>${item.upload_time}</td>
            </tr>`;
            tableBody.innerHTML += row;
        });
    } catch (error) {
        console.error("Error fetching logs:", error);
    }
}

// Load logs when page opens
window.onload = fetchLogs;