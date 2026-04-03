import Sidebar from "./Sidebar";

export default function RootLayout({
  children,
  onHistorySelect,
}: {
  children: React.ReactNode;
  onHistorySelect: (text: string) => void;
}) {
  return (
    <div className="flex">
      <Sidebar onSelect={onHistorySelect} />

      <div className="flex-1 flex justify-center px-4">
        <div className="max-w-4xl w-full py-10">{children}</div>
      </div>
    </div>
  );
}
