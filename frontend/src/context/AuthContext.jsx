import { createContext, useContext, useEffect, useState } from "react";

import {
  clearAuthTokens,
  getCurrentUser,
  getStoredAccessToken,
  loginUser,
  saveAuthTokens,
} from "../api/auth";


const AuthContext = createContext(null);


export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);


  useEffect(() => {
    const loadUser = async () => {
      const token = getStoredAccessToken();

      if (!token) {
        setLoading(false);
        return;
      }

      try {
        const currentUser = await getCurrentUser();
        setUser(currentUser);
      } catch {
        clearAuthTokens();
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    loadUser();
  }, []);


  const login = async (email, password) => {
    const tokens = await loginUser(email, password);

    saveAuthTokens(tokens);

    const currentUser = await getCurrentUser();

    setUser(currentUser);

    return currentUser;
  };


  const logout = () => {
    clearAuthTokens();
    setUser(null);
  };


  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        logout,
        isAuthenticated: Boolean(user),
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}


export function useAuth() {
  return useContext(AuthContext);
}
