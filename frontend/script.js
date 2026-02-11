const API_BASE = "http://127.0.0.1:8000";

const urlInput = document.getElementById("urlInput");
const btnInternal = document.getElementById("btnInternal");
const btnExternal = document.getElementById("btnExternal");
const btnVuln = document.getElementById("btnVuln");
const btnSafe = document.getElementById("btnSafe");
const btnClear = document.getElementById("btnClear");

const output = document.getElementById("output");
const loading = document.getElementById("loading");
const metaEndpoint = document.getElementById("metaEndpoint");
const metaHttp = document.getElementById("metaHttp");

const INTERNAL_URL = "http://127.0.0.1:5001/admin/secret";
const EXTERNAL_URL = "https://example.com";

// Función que deshabilita los botones mientras la llamada está en curso y
// los vuelve a habilitar cuando finaliza.
function setLoading(isLoading) {
  loading.classList.toggle("hidden", !isLoading);
  btnVuln.disabled = isLoading;
  btnSafe.disabled = isLoading;
  btnInternal.disabled = isLoading;
  btnExternal.disabled = isLoading;
  btnClear.disabled = isLoading;
}

// Función que decodifica el mensaje que se le pasa por parámetro para devolverlo
// como un JSON entendible para un humano.
function pretty(obj) {
  return JSON.stringify(obj, null, 2);
}

function setMeta(endpoint, httpText) {
  metaEndpoint.textContent = endpoint ?? "—";
  metaHttp.textContent = httpText ?? "—";
}

// Función que se encarga de llamar al endpoint juntando el path y la url objetivo
// que se le pasan por parámetro.
async function callEndpoint(path, targetUrl) {
  if (!targetUrl || !targetUrl.trim()) {
    output.textContent = "⚠️ Introduce una URL primero.";
    return;
  }

  const endpointUrl = `${API_BASE}${path}?url=${encodeURIComponent(targetUrl.trim())}`;
  setMeta(path, "—");
  setLoading(true);
  output.textContent = "";

  try {
    const res = await fetch(endpointUrl, { method: "GET" });

    const text = await res.text();
    let body;
    try {
      body = JSON.parse(text);
    } catch {
      body = { raw: text };
    }

    setMeta(path, `${res.status} ${res.ok ? "(OK)" : "(ERROR)"}`);
    output.textContent = pretty(body);
  } catch (err) {
    setMeta(path, "NETWORK ERROR");
    output.textContent = pretty({ error: String(err) });
  } finally {
    setLoading(false);
  }
}

// EVENTOS DE LOS BOTONES
btnInternal.addEventListener("click", () => {
  urlInput.value = INTERNAL_URL;
});

btnExternal.addEventListener("click", () => {
  urlInput.value = EXTERNAL_URL;
});

btnVuln.addEventListener("click", () => callEndpoint("/fetch-vuln", urlInput.value));
btnSafe.addEventListener("click", () => callEndpoint("/fetch-safe", urlInput.value));

btnClear.addEventListener("click", () => {
  urlInput.value = "";
  setMeta(null, null);
  output.textContent = "Introduce una URL y pulsa uno de los botones.";
});
