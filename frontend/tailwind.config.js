/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        primary: {
          DEFAULT: "#06b6d4", // cyan-500
          foreground: "#ffffff",
        },
        secondary: {
          DEFAULT: "#1e293b", // slate-800
          foreground: "#f8fafc",
        },
        destructive: {
          DEFAULT: "#f43f5e", // rose-500
          foreground: "#ffffff",
        },
        muted: {
          DEFAULT: "#0f172a", // slate-900
          foreground: "#94a3b8",
        },
        accent: {
          DEFAULT: "#10b981", // emerald-500
          foreground: "#ffffff",
        },
        warning: {
          DEFAULT: "#f59e0b", // amber-500
          foreground: "#000000",
        },
      },
      fontFamily: {
        mono: ["var(--font-mono)", "Menlo", "Consolas", "Courier New", "monospace"],
      },
    },
  },
  plugins: [],
};
