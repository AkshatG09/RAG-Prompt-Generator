import { Sun, Moon } from "lucide-react";
import { useTheme } from "next-themes";

export default function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  return (
    <div className="flex gap-2">
      <button onClick={() => setTheme("light")}>
        <Sun size={18} />
      </button>
      <button onClick={() => setTheme("dark")}>
        <Moon size={18} />
      </button>
    </div>
  );
}
