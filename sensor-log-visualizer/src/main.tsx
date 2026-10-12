import React from "react";
import ReactDOM from "react-dom/client";
import { MantineProvider, createTheme } from "@mantine/core";
import "@mantine/core/styles.css";
import "./App.css";

import App from "./App";

const theme = createTheme({
  primaryColor: "blue",
  fontFamily: 'Inter, "Segoe UI", Arial, sans-serif',
  headings: {
    fontFamily: 'Inter, "Segoe UI", Arial, sans-serif',
    fontWeight: "600",
  },
  defaultRadius: "md",
});

ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement,
).render(
  <React.StrictMode>
    <MantineProvider theme={theme}>
      <App />
    </MantineProvider>
  </React.StrictMode>,
);
