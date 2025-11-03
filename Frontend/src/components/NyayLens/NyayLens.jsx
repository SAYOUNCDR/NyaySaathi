import React, { useState, useRef, useEffect } from "react";
import Nav from "../Navbar/Nav";
import SideBar from "../Sidebar/SideBar";
import { lensUpload, streamLens, getLensStatus } from "../../lib/api";

export default function NyayLens() {
  const [lensId, setLensId] = useState(null);
  const [title, setTitle] = useState("");
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState("");
  const bottomRef = useRef(null);
  const dropRef = useRef(null);
  const inputRef = useRef(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const [ready, setReady] = useState(false);
  const [ingest, setIngest] = useState({ stage: "start", total_chunks: 0, ingested: 0, percent: 0, eta_seconds: null });

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function doUpload(f) {
    if (!f) return;
    setError("");
    // Basic size/type guard (50 MB)
    if (f.size > 50 * 1024 * 1024) {
      setError("File too large (max 50 MB)");
      return;
    }
    // Reset state for a fresh lens session
    setMessages([]);
    setReady(false);
    setIsUploading(true);
    setProgress(0);
    try {
      const res = await lensUpload(f, title || f.name, (pct) => setProgress(pct));
      setLensId(res.lens_id);
      // Poll status until ready
      let tries = 0;
      const poll = async () => {
        try {
          const s = await getLensStatus(res.lens_id);
          if (s.status === "ready") {
            setReady(true);
            return;
          }
          if (s.status === "error") {
            setError(s.message || "Ingestion error");
            return;
          }
          // Update ingest progress details
          setIngest({
            stage: s.stage || "processing",
            total_chunks: s.total_chunks || 0,
            ingested: s.ingested || 0,
            percent: s.percent || 0,
            eta_seconds: s.eta_seconds ?? null,
          });
        } catch {
          // ignore transient errors while polling
        }
        // Keep polling; no arbitrary time caps or estimates
        if (tries++ < 1800) { // ~30 minutes safety cap
          setTimeout(poll, 1000);
        }
      };
      poll();
    } catch {
      setError("Upload failed. Please try again.");
    } finally {
      setIsUploading(false);
    }
  }

  // Upload is triggered automatically on drop/select via doUpload

  function sendMessage(text) {
    const q = text.trim();
    if (!q || !lensId || isStreaming) return;
    setMessages((m) => [...m, { role: "user", content: q }]);
    setInput("");
    setIsStreaming(true);
  /* const stop = */ streamLens(lensId, q, (t) => {
      setMessages((m) => {
        if (m.length > 0 && m[m.length - 1].role === "assistant") {
          const copy = m.slice();
          copy[copy.length - 1] = {
            ...copy[copy.length - 1],
            content: (copy[copy.length - 1].content || "") + t,
          };
          return copy;
        }
        return [...m, { role: "assistant", content: t }];
      });
    }, () => setIsStreaming(false));
    // optional: store stop if you want to cancel
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage(input);
    }
  }

  return (
    <div className="min-h-screen bg-white">
      <Nav />
      <SideBar initialCollapsed />
      <main className="pt-16 pl-16 sm:pl-20 lg:pl-0">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 py-8">
          <div className="text-xs text-[#99BACE] mt-4">Home &gt; LegalLens</div>

          <h1 className="text-3xl sm:text-4xl font-semibold text-[#0A2B42] text-center mt-8">LegalLens</h1>
          <p className="text-[#2C6BA1] text-center mt-3 max-w-2xl mx-auto">
            Upload your legal document and our AI will instantly analyze it for high-risk clauses, confusing language, and key terms.
          </p>

          {!lensId && (
            <div className="flex items-center justify-center mt-10">
              <div
                ref={dropRef}
                onDragOver={(e)=>{e.preventDefault(); setIsDragOver(true);}}
                onDragLeave={()=>setIsDragOver(false)}
                onDrop={(e)=>{e.preventDefault(); setIsDragOver(false); const f = e.dataTransfer.files?.[0]; if (f) doUpload(f);} }
                className={`w-full max-w-3xl rounded-2xl border ${isDragOver? 'border-[#2C6BA1]':'border-[#E6EEF6]'} bg-[#EFF6FB]/60 p-10 sm:p-14 flex flex-col items-center text-center shadow-sm`}
              >
                <img src="/doc.svg" alt="doc" className="w-16 h-16 opacity-80" onError={(e)=>{e.currentTarget.style.display='none';}} />
                <div className="mt-4 text-[#0A2B42] font-semibold text-lg">Drag &amp; drop your PDF* file here</div>
                <div className="text-xs text-[#99BACE] mt-1">*Max file up to 50 MB</div>
                <div className="mt-6">
                  <button
                    type="button"
                    onClick={()=>!isUploading && inputRef.current?.click()}
                    className={`bg-white border border-[#2C6BA1] text-[#2C6BA1] hover:bg-[#F1F7FB] font-medium rounded px-5 py-2 ${isUploading? 'opacity-60 cursor-not-allowed':''}`}
                  >
                    {isUploading ? 'Uploading...' : 'Browse File'}
                  </button>
                  <input
                    ref={inputRef}
                    type="file"
                    accept=".pdf,.docx,.txt,.md"
                    className="hidden"
                    onChange={(e)=>{ const f=e.target.files?.[0]; if (f) doUpload(f);} }
                  />
                </div>
                <div className="mt-6 w-full max-w-md">
                  <label className="block text-xs text-[#99BACE] mb-1 text-left">Title (optional)</label>
                  <input value={title} onChange={(e)=>setTitle(e.target.value)} disabled={isUploading} className="w-full border border-[#E6EEF6] rounded px-3 py-2 disabled:opacity-60" placeholder="Document title" />
                </div>
                {isUploading && (
                  <div className="mt-6 w-full max-w-md text-left">
                    <div className="text-xs text-[#99BACE] mb-1">
                      {progress < 100 ? (
                        <>Uploading: {progress}%</>
                      ) : (
                        <span className="animate-pulse">Processing document (parsing and indexing)...</span>
                      )}
                    </div>
                    <div className="w-full h-2 bg-white/70 rounded-full overflow-hidden border border-[#E6EEF6]">
                      <div className="h-full bg-[#2C6BA1] transition-all duration-200" style={{ width: `${progress}%` }} />
                    </div>
                  </div>
                )}
                {error && <div className="mt-4 text-sm text-red-600">{error}</div>}
              </div>
            </div>
          )}

        {lensId && !ready && (
          <div className="mt-10">
            <div className="text-sm text-[#99BACE]">Lens ID: {lensId}</div>
            <div className="mt-4 rounded-2xl border border-[#E6EEF6] bg-[#EFF6FB]/60 p-8 flex flex-col items-center text-center shadow-sm">
              <div className="h-8 w-8 rounded-full border-2 border-[#2C6BA1] border-t-transparent animate-spin" />
              <div className="mt-4 text-[#0A2B42] font-semibold text-lg">Ingesting your document…</div>
              <div className="text-xs text-[#99BACE] mt-1">Parsing, splitting, embedding and indexing into your private lens.</div>
              <div className="mt-6 w-full max-w-md text-left space-y-2">
                {/* Upload progress (if still running) */}
                {progress > 0 && progress < 100 && (
                  <div>
                    <div className="text-xs text-[#99BACE] mb-1">Uploading: {progress}%</div>
                    <div className="w-full h-2 bg-white/70 rounded-full overflow-hidden border border-[#E6EEF6]">
                      <div className="h-full bg-[#2C6BA1] transition-all duration-200" style={{ width: `${progress}%` }} />
                    </div>
                  </div>
                )}
                {/* Ingestion progress (chunks ingested) */}
                <div>
                  <div className="text-xs text-[#99BACE] mb-1">
                    {ingest.total_chunks > 0
                      ? `Ingested: ${ingest.ingested} / ${ingest.total_chunks} ${ingest.stage ? `• stage: ${ingest.stage}` : ''}`
                      : (progress >= 100 ? 'Preparing chunks…' : 'Waiting for upload to finish…')}
                  </div>
                  <div className="w-full h-2 bg-white/70 rounded-full overflow-hidden border border-[#E6EEF6]">
                    <div className="h-full bg-[#2C6BA1] transition-all duration-200" style={{ width: `${ingest.total_chunks > 0 ? ingest.percent : 0}%` }} />
                  </div>
                </div>
                {Number.isFinite(ingest.eta_seconds) && ingest.eta_seconds != null && (
                  <div className="text-xs text-[#99BACE]">Estimated time remaining: ~{Math.max(0, Math.round(ingest.eta_seconds))}s</div>
                )}
              </div>
              {error && <div className="mt-4 text-sm text-red-600">{error}</div>}
              <button
                type="button"
                onClick={() => { setLensId(null); setReady(false); setMessages([]); setInput(""); setProgress(0); }}
                className="mt-6 bg-white border border-[#2C6BA1] text-[#2C6BA1] hover:bg-[#F1F7FB] font-medium rounded px-5 py-2"
              >Cancel &amp; Upload Another</button>
            </div>
          </div>
        )}

        {lensId && ready && (
          <div className="mt-6">
            <div className="text-sm text-[#99BACE] mb-2">Lens ready • ID: {lensId}</div>
            <div className="space-y-3 mb-4">
              {messages.map((m, i) => (
                <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`rounded-lg p-3 max-w-[80%] whitespace-pre-wrap ${m.role === 'user' ? 'bg-white border border-[#E6EEF6]' : 'bg-[#E7F3FB]'}`}>{m.content}</div>
                </div>
              ))}
              <div ref={bottomRef} />
            </div>
            <div className="bg-white border border-[#EEF6FB] rounded-xl p-3 shadow-sm flex gap-3">
              <textarea value={input} onChange={(e)=>setInput(e.target.value)} onKeyDown={handleKeyDown} rows={1} placeholder="Ask about your document..." className="flex-1 outline-none resize-none" />
              <button onClick={()=>sendMessage(input)} disabled={isStreaming || !lensId} className="bg-[#0A2B42] text-white px-4 py-2 rounded disabled:opacity-60">Send</button>
            </div>
          </div>
        )}
        </div>
      </main>
    </div>
  );
}
