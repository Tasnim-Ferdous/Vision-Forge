let currentEffect = 'normal';
const intensitySlider = document.getElementById('intensity-slider');
const intensityContainer = document.getElementById('intensity-container');
const intensityValueDisplay = document.getElementById('intensity-value');
const videoElem = document.getElementById('video');
const splitToggle = document.getElementById('splitToggle');

function setEffect(effect) {
  currentEffect = effect;
  updateButtons();
  updateIntensityVisibility();
  sendFilterToServer(currentEffect, parseInt(intensitySlider.value));
}

function updateButtons() {
  const effects = ['normal', 'grayscale', 'canny', 'invert', 'blur', 'face', 'thermal', 'face_overlay'];
  effects.forEach(e => {
    const btn = document.getElementById('btn-' + e);
    if (btn) {
      btn.classList.toggle('active', e === currentEffect);
    }
  });
}

function updateIntensityVisibility() {
  if (['blur', 'canny', 'invert', 'thermal'].includes(currentEffect)) {
    intensityContainer.style.display = 'block';
  } else {
    intensityContainer.style.display = 'none';
  }
}

intensitySlider.addEventListener('input', () => {
  intensityValueDisplay.textContent = intensitySlider.value;
  sendFilterToServer(currentEffect, parseInt(intensitySlider.value));
});

function sendFilterToServer(effect, intensity) {
  fetch(`/frame?effect=${effect}&intensity=${intensity}`);
}

function capture() {
  const canvas = document.getElementById('canvas');
  const ctx = canvas.getContext('2d');
  canvas.width = videoElem.naturalWidth || 640;
  canvas.height = videoElem.naturalHeight || 480;
  ctx.drawImage(videoElem, 0, 0, canvas.width, canvas.height);
  alert("Captured! Click Download to save the image.");
}

function downloadImage() {
  const canvas = document.getElementById('canvas');
  if (!canvas.width || !canvas.height) {
    alert("Please capture an image first.");
    return;
  }
  const link = document.createElement('a');
  link.download = `visionforge_${currentEffect}.jpg`;
  link.href = canvas.toDataURL('image/jpeg');
  link.click();
}

splitToggle.addEventListener('change', () => {
  videoElem.src = splitToggle.checked ? '/video_feed_split' : '/video_feed';
});

window.onload = () => {
  setEffect('normal');
};
