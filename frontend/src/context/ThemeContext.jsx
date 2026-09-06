import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";


const ThemeContext = createContext(null);


export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState(() => {
    const savedTheme =
      localStorage.getItem("bhudrishti_theme");

    return savedTheme === "dark"
      ? "dark"
      : "light";
  });


  useEffect(() => {
    document.documentElement.setAttribute(
      "data-theme",
      theme
    );

    localStorage.setItem(
      "bhudrishti_theme",
      theme
    );
  }, [theme]);


  const toggleTheme = () => {
    setTheme((currentTheme) =>
      currentTheme === "dark"
        ? "light"
        : "dark"
    );
  };


  const value = useMemo(
    () => ({
      theme,
      setTheme,
      toggleTheme,
    }),
    [theme]
  );


  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
}


export function useTheme() {
  const context =
    useContext(ThemeContext);

  if (!context) {
    throw new Error(
      "useTheme must be used inside ThemeProvider"
    );
  }

  return context;
}