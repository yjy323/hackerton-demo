const sessionId = crypto.randomUUID();
let mediaRecorder, audioChunks = [];

const uploadAudio = async (blob) => {
  const formData = new FormData();
  formData.append("session_id", sessionId);
  formData.append("file", blob, "recording.wav");
  await fetch("/api/upload/audio", { method: "POST", body: formData });
};

document.getElementById("recordBtn").addEventListener("click", async (e) => {
  if (!mediaRecorder || mediaRecorder.state === "inactive") {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.ondataavailable = (event) => audioChunks.push(event.data);
    mediaRecorder.onstop = async () => {
      const blob = new Blob(audioChunks, { type: "audio/wav" });
      await uploadAudio(blob);
      alert("녹음 업로드 완료!");
    };

    mediaRecorder.start();
    e.target.textContent = "⏹ 녹음 종료";
  } else {
    mediaRecorder.stop();
    e.target.textContent = "🎙 녹음 시작";
  }
});

document.getElementById("uploadImageBtn").addEventListener("click", async () => {
  const file = document.getElementById("fileImage").files[0];
  if (!file) return alert("파일을 선택하세요.");
  const formData = new FormData();
  formData.append("session_id", sessionId);
  formData.append("file", file);
  await fetch("/api/upload/document", { method: "POST", body: formData });
  alert("파일 업로드 완료!");
});

document.getElementById("analyzeBtn").addEventListener("click", async () => {
  document.getElementById("loading").classList.remove("hidden");
  const res = await fetch(`/api/analyze/session/${sessionId}`, { method: "POST" });
  const data = await res.json();

  document.getElementById("loading").classList.add("hidden");
  document.getElementById("result").classList.remove("hidden");
  document.getElementById("summary").innerText = data.summary || "요약 정보가 없습니다.";

  // risks가 없으면 빈 리스트 표시
  const risksHtml = data.risks ? data.risks.map(r => `<li>${r}</li>`).join("") : "<li>위험 요소를 분석할 수 없습니다.</li>";
  document.getElementById("risks").innerHTML = risksHtml;
});
