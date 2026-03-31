import { useEffect, useState } from "react";

export default function StreamingOutput({ text }: { text: string }) {
  const [display, setDisplay] = useState("");

  useEffect(() => {
    let i = 0;
    const interval = setInterval(() => {
      setDisplay(text.slice(0, i));
      i++;
      if (i > text.length) clearInterval(interval);
    }, 10);

    return () => clearInterval(interval);
  }, [text]);

  return (
    <div className="glass p-5 mt-6">
      <pre className="whitespace-pre-wrap text-sm">{display}</pre>
    </div>
  );
}
