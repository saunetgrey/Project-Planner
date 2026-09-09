const sex = document.getElementById('sex');
const hipField = document.getElementById('hip-field');
const hip = document.getElementById('hip');

function updateMeasurements() {
  const needsHips = sex.value === 'female';
  hipField.hidden = !needsHips;
  hip.required = needsHips;
  hip.disabled = !needsHips;
}

sex.addEventListener('change', updateMeasurements);
updateMeasurements();
