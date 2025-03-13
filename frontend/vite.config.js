import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0",  // Ensures it's accessible from other devices
    port: 5174,  // Must match the port you are running
    strictPort: true,
    watch: {
      usePolling: true,  // Helps fix issues with file updates in some environments
    },
  },
});
