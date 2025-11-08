import React, { useEffect, useState } from "react";

export default function History() {
  const [items, setItems] = useState([]);

  const load = async () => {
    const res = await fetch("http://localhost:5000/history");
    const data = await res.json();
    if (Array.isArray(data)) setItems(data);
  };

  useEffect(() => {
    load();
    setInterval(load, 3000);
  }, []);

  return (
    <div className="bg-white w-full lg:w-2/5 p-6 rounded-xl shadow-md">
      <h3 className="font-semibold text-lg mb-4">Recent Scans ({items.length})</h3>

      <div className="h-[400px] overflow-y-scroll space-y-3">
        {items.length === 0 && <p>No scans yet</p>}

        {items.map((x, i) => (
          <div key={i} className="flex gap-3 bg-gray-50 p-2 rounded shadow-sm">
            <img src={x.image} className="w-20 h-20 object-cover rounded" />
            <div>
              <h4 className="font-semibold">{x.label}</h4>
              <p className="text-sm text-gray-500">{(x.confidence * 100).toFixed(2)}%</p>
              <p className="text-xs text-gray-400">{x.time}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
