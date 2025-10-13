import { useState } from "react";
import axios from "axios";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { toast } from "sonner";
import { GraduationCap, UserCircle, Shield } from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const LoginPage = ({ onLogin }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [showCredentials, setShowCredentials] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await axios.post(`${API}/auth/login`, {
        username,
        password,
      });

      if (response.data.success) {
        toast.success(`Welcome ${response.data.user.name}!`);
        onLogin(response.data.user);
      } else {
        toast.error(response.data.message || "Invalid credentials");
      }
    } catch (error) {
      console.error("Login error:", error);
      toast.error("Failed to login. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const quickLogin = (user, pass) => {
    setUsername(user);
    setPassword(pass);
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4" style={{ background: 'linear-gradient(135deg, #e0f2fe 0%, #fae8ff 50%, #fef3c7 100%)' }}>
      <div className="w-full max-w-5xl grid md:grid-cols-2 gap-8 items-center">
        {/* Left side - Welcome */}
        <div className="text-center md:text-left space-y-6">
          <div className="inline-block p-4 bg-white/80 backdrop-blur-sm rounded-3xl shadow-lg">
            <GraduationCap className="w-16 h-16 text-indigo-600" />
          </div>
          <div>
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 mb-4">
              CollegeMate
            </h1>
            <p className="text-base sm:text-lg text-gray-700 max-w-md">
              Your all-in-one campus convenience platform for students, teachers, and administrators
            </p>
          </div>
          
          {/* Quick access demo credentials */}
          <div className="space-y-3 pt-4">
            <p className="text-sm font-semibold text-gray-600">Quick Demo Login:</p>
            <div className="flex flex-wrap gap-2">
              <Button
                data-testid="quick-login-student"
                variant="outline"
                size="sm"
                onClick={() => quickLogin("ai", "alicepw")}
                className="gap-2"
              >
                <UserCircle className="w-4 h-4" />
                Student
              </Button>
              <Button
                data-testid="quick-login-teacher"
                variant="outline"
                size="sm"
                onClick={() => quickLogin("ai", "vkumarpw")}
                className="gap-2"
              >
                <UserCircle className="w-4 h-4" />
                Teacher
              </Button>
              <Button
                data-testid="quick-login-admin"
                variant="outline"
                size="sm"
                onClick={() => quickLogin("ai", "srinipw")}
                className="gap-2"
              >
                <Shield className="w-4 h-4" />
                Admin
              </Button>
            </div>
            <button
              data-testid="show-all-credentials-btn"
              onClick={() => setShowCredentials(!showCredentials)}
              className="text-sm text-indigo-600 hover:underline"
            >
              {showCredentials ? "Hide" : "Show"} all demo credentials
            </button>
          </div>
        </div>

        {/* Right side - Login Form */}
        <Card data-testid="login-card" className="shadow-2xl border-0">
          <CardHeader className="space-y-2">
            <CardTitle className="text-2xl">Login to Your Account</CardTitle>
            <CardDescription>Enter your credentials to access the portal</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleLogin} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="username">Username</Label>
                <Input
                  data-testid="username-input"
                  id="username"
                  type="text"
                  placeholder="Enter username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <Input
                  data-testid="password-input"
                  id="password"
                  type="password"
                  placeholder="Enter password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
              <Button
                data-testid="login-submit-btn"
                type="submit"
                className="w-full"
                disabled={loading}
              >
                {loading ? "Logging in..." : "Login"}
              </Button>
            </form>

            {showCredentials && (
              <div data-testid="credentials-panel" className="mt-6 p-4 bg-gray-50 rounded-lg space-y-3 text-xs">
                <p className="font-semibold text-gray-700">Demo Credentials:</p>
                <div className="space-y-2">
                  <div>
                    <p className="font-medium text-gray-600">Students:</p>
                    <p>Alice James: ai / alicepw</p>
                    <p>Bob Wilson: bob / bobpw</p>
                    <p>Carol Martinez: carol / carolpw</p>
                  </div>
                  <div>
                    <p className="font-medium text-gray-600">Teachers:</p>
                    <p>Prof. V. Kumar: ai / vkumarpw</p>
                    <p>Dr. S. Rajamanickam: sraja / srajapw</p>
                  </div>
                  <div>
                    <p className="font-medium text-gray-600">Admin:</p>
                    <p>V. Srinivasan: ai / srinipw</p>
                  </div>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default LoginPage;