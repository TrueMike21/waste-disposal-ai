const fileInput = document.getElementById('file-input');
const preview = document.getElementById('preview');
const analyzeBtn = document.getElementById('analyze-btn');
const dropZone = document.getElementById('drop-zone');
const dropText = document.getElementById('drop-text');
const result = document.getElementById('result');

let selectedFile = null;

fileInput.addEventListener('change', e => handleFile(e.target.files[0]));

dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.style.background = '#f1f8f1'; });
dropZone.addEventListener('drop', e => {
  e.preventDefault();
  handleFile(e.dataTransfer.files[0]);
});

function handleFile(file) {
  if (!file) return;
  selectedFile = file;
  const reader = new FileReader();
  reader.onload = e => {
    preview.src = e.target.result;
    preview.hidden = false;
    dropText.hidden = true;
    analyzeBtn.disabled = false;
  };
  reader.readAsDataURL(file);
}

analyzeBtn.addEventListener('click', async () => {
  if (!selectedFile) return;
  analyzeBtn.textContent = 'Analyzing...';
  analyzeBtn.disabled = true;

  const formData = new FormData();
  formData.append('file', selectedFile);

  try {
    const res = await fetch('/predict', { method: 'POST', body: formData });
    const data = await res.json();
    displayResult(data);
  } catch (err) {
    alert('Error contacting the server. Is Flask running?');
  } finally {
    analyzeBtn.textContent = 'Analyze Waste';
    analyzeBtn.disabled = false;
  }
});

function displayResult(data) {
  document.getElementById('result-category').textContent = data.category || 'Unknown';
  document.getElementById('result-bin').textContent = `🗂 Bin: ${data.bin_color || 'N/A'}`;

  const ul = document.getElementById('result-instructions');
  ul.innerHTML = '';
  (data.instructions || []).forEach(i => {
    const li = document.createElement('li');
    li.textContent = i;
    ul.appendChild(li);
  });

  const warnEl = document.getElementById('result-warning');
  if (data.warning) {
    warnEl.textContent = data.warning;
    warnEl.hidden = false;
  } else {
    warnEl.hidden = true;
  }

  document.getElementById('result-confidence').textContent =
    data.confidence ? `Model confidence: ${data.confidence}%` : '';

  result.hidden = false;
}