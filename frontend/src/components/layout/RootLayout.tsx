import Sidebar from "./Sidebar";

export default function RootLayout({ children }: any) {
  return (
    <div className="flex">
      <Sidebar onSelect={(text) => console.log(text)} />

      <div className="flex-1 flex justify-center px-4">
        <div className="max-w-4xl w-full py-10">{children}</div>
      </div>
    </div>
  );
}
