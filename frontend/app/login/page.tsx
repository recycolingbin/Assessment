'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { authAPI } from '@/lib/api';

declare global {
  interface Window {
    google: any;
  }
}

export default function LoginPage() {
  const router = useRouter();
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({ email: '', username: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [passwordStrength, setPasswordStrength] = useState({ score: 0, message: '' });
  const [showVerificationMessage, setShowVerificationMessage] = useState(false);
  const [showResendLink, setShowResendLink] = useState(false);
  const [unverifiedEmail, setUnverifiedEmail] = useState('');

  useEffect(() => {
    // Load Google Sign-In script
    const script = document.createElement('script');
    script.src = 'https://accounts.google.com/gsi/client';
    script.async = true;
    script.defer = true;
    document.body.appendChild(script);

    script.onload = () => {
      if (window.google) {
        window.google.accounts.id.initialize({
          client_id: process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID || '',
          callback: handleGoogleSignIn,
        });
        window.google.accounts.id.renderButton(
          document.getElementById('googleSignInButton'),
          { theme: 'outline', size: 'large', width: '100%', text: 'continue_with', shape: 'rectangular' }
        );
      }
    };

    return () => {
      if (document.body.contains(script)) {
        document.body.removeChild(script);
      }
    };
  }, []);

  const validatePassword = (password: string) => {
    let score = 0;
    let message = '';

    if (password.length >= 8) score++;
    if (/[A-Z]/.test(password)) score++;
    if (/[a-z]/.test(password)) score++;
    if (/\d/.test(password)) score++;
    if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) score++;

    if (score === 0) message = '';
    else if (score <= 2) message = 'Weak';
    else if (score === 3 || score === 4) message = 'Medium';
    else message = 'Strong';

    setPasswordStrength({ score, message });
  };

  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newPassword = e.target.value;
    setFormData({ ...formData, password: newPassword });
    if (!isLogin) {
      validatePassword(newPassword);
    }
  };

  const handleGoogleSignIn = async (response: any) => {
    setError('');
    setLoading(true);
    try {
      const result = await authAPI.googleAuth(response.credential);
      localStorage.setItem('token', result.data.access_token);
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Google sign-in failed');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setShowResendLink(false);
    setLoading(true);
    try {
      if (isLogin) {
        const response = await authAPI.login({ email: formData.email, password: formData.password });
        localStorage.setItem('token', response.data.access_token);
        router.push('/dashboard');
      } else {
        await authAPI.register({ email: formData.email, username: formData.username, password: formData.password });
        setShowVerificationMessage(true);
        setError('');
      }
    } catch (err: any) {
      const errorDetail = err.response?.data?.detail;
      if (typeof errorDetail === 'string') {
        setError(errorDetail);
        if (errorDetail.includes('verify your email')) {
          setShowResendLink(true);
          setUnverifiedEmail(formData.email);
        }
      } else if (Array.isArray(errorDetail)) {
        setError(errorDetail.map((e: any) => e.msg).join(', '));
      } else {
        setError('An error occurred. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleResendVerification = async () => {
    setLoading(true);
    setError('');
    try {
      await authAPI.resendVerification(unverifiedEmail);
      setError('');
      setShowVerificationMessage(true);
      setShowResendLink(false);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to resend verification email');
    } finally {
      setLoading(false);
    }
  };

  if (showVerificationMessage) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 px-4">
        <div className="w-full max-w-md">
          <div className="bg-white rounded-2xl shadow-xl border border-slate-200 p-8 text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-blue-100 mb-6">
              <svg className="w-8 h-8 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <h1 className="text-2xl font-semibold text-slate-900 mb-3">Check Your Email</h1>
            <p className="text-slate-600 mb-4 leading-relaxed">
              We've sent a verification link to <strong className="text-slate-900">{formData.email}</strong>.
              Please check your inbox and click the link to verify your account.
            </p>
            <p className="text-sm text-slate-500 mb-6">
              Please check your inbox and spam folder. The link will expire in 1 hour.
            </p>
            <button
              onClick={() => setShowVerificationMessage(false)}
              className="w-full py-3 px-4 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors"
            >
              Back to Login
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Left side - Branding */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800 p-12 flex-col justify-between relative overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-0 left-0 w-96 h-96 bg-white rounded-full blur-3xl -translate-x-1/2 -translate-y-1/2" />
          <div className="absolute bottom-0 right-0 w-96 h-96 bg-indigo-300 rounded-full blur-3xl translate-x-1/2 translate-y-1/2" />
        </div>

        <div className="relative z-10">
          <div className="flex items-center gap-3 mb-8">
            <div className="w-10 h-10 bg-white rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
            </div>
            <span className="text-2xl font-bold text-white">PortfolioIQ</span>
          </div>

          <h1 className="text-4xl font-bold text-white mb-4 leading-tight">
            Professional Portfolio<br />Management Platform
          </h1>
          <p className="text-blue-100 text-lg leading-relaxed">
            Trusted by financial professionals worldwide to track, analyze, and optimize investment portfolios with institutional-grade tools.
          </p>
        </div>

        <div className="relative z-10 grid grid-cols-3 gap-6">
          <div className="text-center">
            <div className="text-3xl font-bold text-white mb-1">$2.5B+</div>
            <div className="text-blue-200 text-sm">Assets Tracked</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-white mb-1">50K+</div>
            <div className="text-blue-200 text-sm">Active Users</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-white mb-1">99.9%</div>
            <div className="text-blue-200 text-sm">Uptime</div>
          </div>
        </div>
      </div>

      {/* Right side - Form */}
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="w-full max-w-md">
          {/* Mobile logo */}
          <div className="lg:hidden flex items-center gap-3 mb-8 justify-center">
            <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
            </div>
            <span className="text-2xl font-bold text-slate-900">PortfolioIQ</span>
          </div>

          <div className="bg-white rounded-2xl shadow-xl border border-slate-200 p-8">
            <div className="mb-8">
              <h2 className="text-2xl font-semibold text-slate-900 mb-2">
                {isLogin ? 'Welcome back' : 'Create your account'}
              </h2>
              <p className="text-slate-600">
                {isLogin ? 'Sign in to access your portfolio' : 'Start managing your investments today'}
              </p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-5">
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-slate-700 mb-2">
                  Email address
                </label>
                <input
                  id="email"
                  type="email"
                  placeholder="you@example.com"
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all text-slate-900 placeholder-slate-400"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  required
                />
              </div>

              {!isLogin && (
                <div>
                  <label htmlFor="username" className="block text-sm font-medium text-slate-700 mb-2">
                    Username
                  </label>
                  <input
                    id="username"
                    type="text"
                    placeholder="johndoe"
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all text-slate-900 placeholder-slate-400"
                    value={formData.username}
                    onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                    required
                  />
                </div>
              )}

              <div>
                <label htmlFor="password" className="block text-sm font-medium text-slate-700 mb-2">
                  Password
                </label>
                <input
                  id="password"
                  type="password"
                  placeholder="••••••••"
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all text-slate-900 placeholder-slate-400"
                  value={formData.password}
                  onChange={handlePasswordChange}
                  required
                />
                {!isLogin && formData.password && (
                  <div className="mt-2">
                    <div className="flex items-center gap-2 mb-1">
                      <div className="flex-1 h-1.5 bg-slate-200 rounded-full overflow-hidden">
                        <div
                          className={`h-full transition-all ${passwordStrength.score <= 2 ? 'bg-red-500 w-1/3' :
                            passwordStrength.score <= 4 ? 'bg-amber-500 w-2/3' : 'bg-emerald-500 w-full'
                            }`}
                        />
                      </div>
                      <span className={`text-xs font-medium ${passwordStrength.score <= 2 ? 'text-red-600' :
                        passwordStrength.score <= 4 ? 'text-amber-600' : 'text-emerald-600'
                        }`}>
                        {passwordStrength.message}
                      </span>
                    </div>
                  </div>
                )}
              </div>

              {isLogin && (
                <div className="flex items-center justify-end">
                  <button
                    type="button"
                    onClick={() => router.push('/forgot-password')}
                    className="text-sm text-blue-600 hover:text-blue-700 font-medium"
                  >
                    Forgot password?
                  </button>
                </div>
              )}

              {error && (
                <div className="rounded-lg bg-red-50 border border-red-200 px-4 py-3 text-red-700 text-sm">
                  <div className="flex items-start gap-2">
                    <svg className="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <div className="flex-1">
                      <p>{error}</p>
                      {showResendLink && (
                        <button
                          type="button"
                          onClick={handleResendVerification}
                          disabled={loading}
                          className="mt-2 text-blue-600 hover:text-blue-700 underline font-medium disabled:opacity-50"
                        >
                          Resend verification email
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              )}

              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 px-4 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {loading && (
                  <svg className="w-5 h-5 animate-spin" viewBox="0 0 24 24" fill="none">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
                  </svg>
                )}
                {isLogin ? 'Sign in' : 'Create account'}
              </button>
            </form>

            <div className="mt-6">
              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-slate-300" />
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-4 bg-white text-slate-500">Or continue with</span>
                </div>
              </div>

              <div className="mt-6">
                <div id="googleSignInButton" className="w-full" />
              </div>
            </div>

            <div className="mt-6 text-center">
              <button
                type="button"
                onClick={() => { setIsLogin(!isLogin); setError(''); setPasswordStrength({ score: 0, message: '' }); }}
                className="text-sm text-slate-600 hover:text-slate-900"
              >
                {isLogin ? "Don't have an account? " : 'Already have an account? '}
                <span className="text-blue-600 hover:text-blue-700 font-medium">
                  {isLogin ? 'Sign up' : 'Sign in'}
                </span>
              </button>
            </div>
          </div>

          <p className="text-center text-slate-500 text-xs mt-6">
            &copy; {new Date().getFullYear()} PortfolioIQ. All rights reserved.
          </p>
        </div>
      </div>
    </div>
  );
}
