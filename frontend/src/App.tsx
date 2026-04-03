import { useState } from "react";
import RootLayout from "./components/layout/RootLayout";
import GeneratorPage from "./features/generator/GeneratorPage";
import AppToaster from "./components/ui/Toaster";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "./lib/queryClient";

export default function App() {
  const [request, setRequest] = useState("");

  return (
    <QueryClientProvider client={queryClient}>
      <RootLayout onHistorySelect={setRequest}>
        <GeneratorPage request={request} setRequest={setRequest} />
      </RootLayout>
      <AppToaster />
    </QueryClientProvider>
  );
}
