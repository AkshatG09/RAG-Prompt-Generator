import RootLayout from "./components/layout/RootLayout";
import GeneratorPage from "./features/generator/GeneratorPage";
import AppToaster from "./components/ui/Toaster";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "./lib/queryClient";

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <RootLayout>
        <GeneratorPage />
      </RootLayout>
      <AppToaster />
    </QueryClientProvider>
  );
}
