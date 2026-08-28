import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

import "./LoginPage.css";


export default function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);


  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");
    setSubmitting(true);

    try {
      await login(email, password);

      navigate("/dashboard", {
        replace: true,
      });
    } catch (err) {
      setError(
        err?.response?.data?.detail ||
          "Login failed. Please check your credentials."
      );
    } finally {
      setSubmitting(false);
    }
  };


  return (
    <main className="login-page">
      <section className="login-visual">
        <div className="login-brand">
          <div className="login-brand-mark">
            BD
          </div>

          <div>
            <h1>BhuDrishti AI</h1>
            <p>Geo-Hazard Intelligence Platform</p>
          </div>
        </div>

        <div className="login-hero">
          <span className="login-kicker">
            AI � GIS � EARLY WARNING
          </span>

          <h2>
            Predict hazards.
            <br />
            Protect communities.
          </h2>

          <p>
            Geo-hazard intelligence for landslides,
            flash floods, vulnerable roads and communities
            across North-East India.
          </p>
        </div>

        <div className="login-capabilities">
          <div>
            <strong>24/7</strong>
            <span>Monitoring</span>
          </div>

          <div>
            <strong>AI</strong>
            <span>Risk Engine</span>
          </div>

          <div>
            <strong>GIS</strong>
            <span>GIS Mapping</span>
          </div>
        </div>
      </section>


      <section className="login-panel">
        <div className="login-card">
          <div className="login-card-header">
            <span className="login-status">
              <span />
              SYSTEM ONLINE
            </span>

            <h2>Command Center Login</h2>

            <p>
              Sign in to access geo-hazard intelligence and monitoring tools.
            </p>
          </div>


          <form
            className="login-form"
            onSubmit={handleSubmit}
          >
            <div className="login-field">
              <label htmlFor="email">
                Email Address
              </label>

              <input
                id="email"
                type="email"
                value={email}
                onChange={(event) =>
                  setEmail(event.target.value)
                }
                placeholder="name@example.com"
                autoComplete="email"
                required
              />
            </div>


            <div className="login-field">
              <label htmlFor="password">
                Password
              </label>

              <input
                id="password"
                type="password"
                value={password}
                onChange={(event) =>
                  setPassword(event.target.value)
                }
                placeholder="Enter your password"
                autoComplete="current-password"
                required
              />
            </div>


            {error && (
              <div
                className="login-error"
                role="alert"
              >
                {error}
              </div>
            )}


            <button
              className="login-submit"
              type="submit"
              disabled={submitting}
            >
              {submitting
                ? "Signing in..."
                : "Sign In to Command Center"}
            </button>
          </form>


          <div className="login-security">
            Secure authenticated access � Protected API session
          </div>
        </div>
      </section>
    </main>
  );
}

