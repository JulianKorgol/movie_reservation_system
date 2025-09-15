'use client';
import { Button } from "@/components/ui/button";
import React, { useState } from "react";
import {Input} from "@/components/ui/input";
import {authService} from "@/services/auth.service";
import { toast } from "sonner";

export default function LoginForm({ onSwitch }: { onSwitch: any }) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        await new Promise((resolve) => setTimeout(resolve, 1000));

        if (!email) {
            toast.error("Email is required");
            setLoading(false);
            return;
        }
        if (!/\S+@\S+\.\S+/.test(email)) {
            toast.error("Please enter a valid email");
            setLoading(false);
            return;
        }
        if (!password) {
            toast.error("Password is required");
            setLoading(false);
            return;
        }
        if (password.length < 6) {
            toast.error("Password must be at least 6 characters");
            setLoading(false);
            return;
        }


        try {
            const response = await authService.login({ email, password });
            console.log("Login successful:", response);

            localStorage.setItem("authToken", response.token);
            toast.success(`Welcome back, ${response.user.firstName}!`);

            // TODO: redirect to dashboard or home
        } catch (error) {
            console.error("Login failed:", error);
            toast.error("Invalid email or password.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="font-sans min-h-screen p-8 pb-20 gap-16 sm:p-20">
            <header>
                <h1 className="text-3xl font-bold text-center mt-10">Log In</h1>
            </header>

            <form
                onSubmit={handleSubmit}
                className="flex flex-col gap-4 max-w-sm mx-auto mt-20"
                noValidate
            >
                <div>
                    <label
                        htmlFor="email"
                        className="block text-sm font-medium text-gray-700"
                    >
                        Email
                    </label>
                    <Input
                        type="email"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className="mt-1 block w-full"
                        required
                    />
                </div>
                <div>
                    <label
                        htmlFor="password"
                        className="block text-sm font-medium text-gray-700"
                    >
                        Password
                    </label>
                    <Input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="mt-1 block w-full"
                        required
                    />
                </div>
                <Button type="submit" className="w-full" disabled={loading}>
                    {loading ? "Logging in..." : "Log In"}
                </Button>
                <Button
                    type="button"
                    variant="ghost"
                    className="w-full mt-2"
                    onClick={onSwitch}
                >
                    Don&apos;t have an account? Sign Up
                </Button>
            </form>
        </div>
    );
}
