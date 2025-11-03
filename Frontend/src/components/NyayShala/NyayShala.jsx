import React, { useEffect, useState } from "react";
import Nav from "../Navbar/Nav";
import { getDailyNyayShala } from "../../lib/api";

const FIELDS = ["contract", "criminal", "family", "ip", "tax", "property"];

export default function NyayShala() {
  const [field, setField] = useState("");
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  const load = async () => {
    setLoading(true);
    try {
      const data = await getDailyNyayShala(field || undefined);
      setItems(data.items || []);
    } catch (e) {
      console.error(e);
      setItems([]);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(); }, [field]);

  return (
    <div className="min-h-screen bg-white">
      <Nav />
      <main className="pt-16 max-w-4xl mx-auto px-4 py-8">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-semibold text-[#0A2B42]">NyayShala</h1>
          <select value={field} onChange={(e)=>setField(e.target.value)} className="border rounded px-2 py-1">
            <option value="">All Fields</option>
            {FIELDS.map(f=> <option key={f} value={f}>{f}</option>)}
          </select>
        </div>

        {loading ? (
          <div className="mt-6 text-[#99BACE]">Loading...</div>
        ) : (
          <div className="mt-6 space-y-4">
            {items.map((it, idx) => (
              <div key={idx} className="border border-[#EEF6FB] rounded-xl p-4">
                <div className="text-xs uppercase tracking-wide text-[#99BACE]">{it.field}</div>
                <div className="text-lg font-semibold text-[#0A2B42]">{it.title}</div>
                <div className="mt-2 whitespace-pre-wrap text-[#0A2B42]">{it.content}</div>
              </div>
            ))}
            {items.length===0 && (
              <div className="text-[#99BACE]">No items yet. Try generating from admin (coming soon) or check back later.</div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}
