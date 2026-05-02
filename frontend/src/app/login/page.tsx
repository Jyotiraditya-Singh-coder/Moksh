'use client';

import { useState, FormEvent } from 'react';
import Link from 'next/link';
import { SignInButton } from '@clerk/nextjs';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleEmailLogin = (e: FormEvent) => {
    e.preventDefault();
    setError('');
    if (!email || !password) {
      setError('Please fill in all fields.');
      return;
    }
    setLoading(true);
    // TODO: connect to your auth backend
    setTimeout(() => setLoading(false), 1500);
  };

  const handleGoogleLogin = () => {
    // TODO: connect Clerk Google OAuth
    // e.g. window.location.href = '/api/auth/google';
  };

  return (
    <div className="auth-page">
      <div className="auth-container">
        {/* Left decorative panel */}
        <div className="auth-hero">
          <div className="auth-hero-content">
            <Link href="/" className="auth-logo">EduNex AI</Link>
            <h2>Welcome Back</h2>
            <p>Continue your personalized learning journey with AI-powered education.</p>
            <div className="auth-hero-shapes">
              <div className="shape shape-1" />
              <div className="shape shape-2" />
              <div className="shape shape-3" />
            </div>
          </div>
        </div>

        {/* Right form panel */}
        <div className="auth-form-panel">
          <div className="auth-form-wrapper">
            <h1 className="auth-title">Log In</h1>
            <p className="auth-subtitle">Sign in to your account to continue</p>

            {/* Google Sign-In */}
              <SignInButton mode="modal" forceRedirectUrl="/dashboard">
                <button type="button" className="btn-google">
                  <svg width="20" height="20" viewBox="0 0 48 48">
                    <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
                    <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
                    <path fill="#FBBC05" d="M10.53 28.59a14.5 14.5 0 0 1 0-9.18l-7.98-6.19a24.0 24.0 0 0 0 0 21.56l7.98-6.19z"/>
                    <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
                  </svg>
                  Continue with Google
                </button>
              </SignInButton>

            <div className="auth-divider">
              <span>or sign in with email</span>
            </div>

            {/* Email/Password Form */}
            <form onSubmit={handleEmailLogin} className="auth-form">
              {error && <div className="auth-error">{error}</div>}

              <div className="auth-field">
                <label htmlFor="login-email">Email Address</label>
                <input
                  id="login-email"
                  type="email"
                  placeholder="you@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  autoComplete="email"
                  required
                />
              </div>

              <div className="auth-field">
                <label htmlFor="login-password">Password</label>
                <div className="password-wrapper">
                  <input
                    id="login-password"
                    type={showPassword ? 'text' : 'password'}
                    placeholder="--------"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    autoComplete="current-password"
                    required
                  />
                  <button
                    type="button"
                    className="toggle-password"
                    onClick={() => setShowPassword(!showPassword)}
                    aria-label="Toggle password visibility"
                  >
                    {showPassword ? '--' : '---'}
                  </button>
                </div>
              </div>

              <div className="auth-extras">
                <label className="remember-me">
                  <input type="checkbox" /> Remember me
                </label>
                <a href="#" className="forgot-link">Forgot password?</a>
              </div>

              <button
                type="submit"
                className="btn-auth-submit"
                disabled={loading}
              >
                {loading ? 'Signing in-' : 'Sign In'}
              </button>
            </form>

            <p className="auth-switch">
              Don&apos;t have an account?{' '}
              <Link href="/signup">Sign Up</Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
