// Fields must match the model's training column order (without DEATH_EVENT)
const fields = [
  "age",
  "anaemia",
  "creatinine_phosphokinase",
  "diabetes",
  "ejection_fraction",
  "high_blood_pressure",
  "platelets",
  "serum_creatinine",
  "serum_sodium",
  "sex",
  "smoking",
  "time",
];

const fieldsContainer = document.getElementById("fields");
const form = document.getElementById("predict-form");
const resultEl = document.getElementById("result");

function makeField(name) {
  const wrapper = document.createElement("div");
  wrapper.className = "form-group";
  const label = document.createElement("label");
  label.textContent = name.replace(/_/g, " ");
  label.htmlFor = name;

  let input;
  // binary-ish fields
  if (["anaemia", "diabetes", "high_blood_pressure", "sex", "smoking"].includes(name)) {
    input = document.createElement("select");
    input.id = name;
    const opt0 = document.createElement("option"); opt0.value = ""; opt0.textContent = "Select...";
    const opt0val = document.createElement("option"); opt0val.value = "0"; opt0val.textContent = "No";
    const opt1 = document.createElement("option"); opt1.value = "1"; opt1.textContent = "Yes";
    input.appendChild(opt0); input.appendChild(opt0val); input.appendChild(opt1);
  } else {
    input = document.createElement("input");
    input.type = "number";
    input.step = "any";
    input.id = name;
    input.placeholder = "Enter value...";
    input.required = true;
  }

  wrapper.appendChild(label);
  wrapper.appendChild(input);
  return wrapper;
}

fields.forEach(f => fieldsContainer.appendChild(makeField(f)));

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const payload = {};
  for (const f of fields) {
    const el = document.getElementById(f);
    if (!el.value) {
      alert(`Please fill in the ${f.replace(/_/g, " ")} field`);
      return;
    }
    payload[f] = el.value;
  }

  resultEl.innerHTML = '<div class="result-box" style="text-align: center;"><p style="font-size: 16px; margin: 20px 0;">🔄 Analyzing patient data...</p></div>';
  
  try {
    const res = await fetch('/predict', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload)
    });
    if (!res.ok) {
      const txt = await res.text();
      resultEl.innerHTML = `<div class="result-box"><div class="result-title">⚠️ Error</div><p>${txt}</p></div>`;
      return;
    }
    const data = await res.json();
    const prob = data.death_probability * 100;
    const riskLevel = prob > 60 ? 'high-risk' : prob > 30 ? 'moderate-risk' : 'low-risk';
    const riskText = prob > 60 ? '🔴 High Risk' : prob > 30 ? '🟡 Moderate Risk' : '🟢 Low Risk';
    
    // Build factors HTML
    let factorsHTML = '';
    if (data.top_factors && Object.keys(data.top_factors).length > 0) {
      factorsHTML = '<div class="factors-section"><h3 style="margin-top: 20px; margin-bottom: 12px; font-size: 14px; font-weight: 700; color: #2c3e50;">📊 Key Contributing Factors</h3><div class="factors-list">';
      Object.entries(data.top_factors).forEach(([key, factor], idx) => {
        const factorImportance = (factor.importance * 100).toFixed(1);
        factorsHTML += `<div class="factor-item">
          <div class="factor-name">${idx + 1}. ${factor.display_name}</div>
          <div class="factor-details">
            <span class="factor-value">Value: <strong>${typeof factor.value === 'number' ? factor.value.toFixed(2) : factor.value}</strong></span>
            <span class="factor-importance">Influence: <strong>${factorImportance}%</strong></span>
          </div>
          <div class="factor-bar"><div class="factor-bar-fill" style="width: ${factorImportance}%"></div></div>
        </div>`;
      });
      factorsHTML += '</div></div>';
    }
    
    resultEl.innerHTML = `
      <div class="result-box ${riskLevel}">
        <div class="result-title">${riskText}</div>
        <div class="risk-meter">
          <div class="meter-label">
            <span>Risk Level</span>
            <span>${prob.toFixed(1)}%</span>
          </div>
          <div class="meter-bar">
            <div class="meter-fill" style="width: ${prob}%"></div>
          </div>
        </div>
        <div class="result-stats">
          <div class="stat">
            <div class="stat-label">Prediction</div>
            <div class="stat-value">${data.prediction ? 'Positive' : 'Negative'}</div>
          </div>
          <div class="stat">
            <div class="stat-label">Death Probability</div>
            <div class="stat-value">${prob.toFixed(2)}%</div>
          </div>
        </div>
        ${factorsHTML}
        <p style="margin-top: 15px; font-size: 12px; color: #666; line-height: 1.5;">
          ℹ️ This assessment is for clinical decision support only. Always consult with qualified healthcare professionals for definitive diagnosis and treatment plans.
        </p>
      </div>
    `;
  } catch (err) {
    resultEl.innerHTML = `<div class="result-box"><div class="result-title">⚠️ Error</div><p>Failed to connect to the server: ${err.message}</p></div>`;
  }
});
