'use client';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import React, { useState } from "react";
import { authService } from "@/services/auth.service";
import type { SignUpRequest } from "@/models/auth.model";
import { toast } from "sonner";

export default function SignUpForm({ onSwitch }: { onSwitch: any }) {
    const [form, setForm] = useState<SignUpRequest>({
        firstName: "",
        lastName: "",
        email: "",
        password: "",
    });

    const [confirmPassword, setConfirmPassword] = useState("");
    const [loading, setLoading] = useState(false);

    const handleChange = (key: keyof SignUpRequest, value: string) => {
        setForm(prev => ({ ...prev, [key]: value }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        await new Promise((resolve) => setTimeout(resolve, 1000));

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(form.email)) {
            toast.error("Invalid email format!");
            setLoading(false);
            return;
        }

        if (form.password.length < 8) {
            toast.error("Password must be at least 8 characters!");
            setLoading(false);
            return;
        }

        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/;
        if (!passwordRegex.test(form.password)) {
            toast.error("Password must contain uppercase, lowercase, and a number!");
            setLoading(false);
            return;
        }

        if (form.password !== confirmPassword) {
            toast.error("Passwords do not match!");
            setLoading(false);
            return;
        }

        try {
            const response = await authService.signUp(form);
            console.log("Sign-up response:", response);
            toast.success(`Your account has been created.`);
            localStorage.setItem("authToken", response.token);
            // TODO: redirect to dashboard or home page
        } catch (error) {
            console.error("Sign-up failed:", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="font-sans min-h-screen p-8 pb-20 gap-16 sm:p-20">
            <header>
                <h1 className="text-3xl font-bold text-center mt-10">Sign Up</h1>
            </header>

            <form onSubmit={handleSubmit} className="flex flex-col gap-4 max-w-sm mx-auto mt-20" noValidate>
                <div className="flex gap-4">
                    <div className="flex-1">
                        <label htmlFor="first-name" className="block text-sm font-medium text-gray-700">First Name</label>
                        <Input
                            type="text"
                            id="first-name"
                            value={form.firstName}
                            onChange={(e) => handleChange("firstName", e.target.value)}
                            required
                        />
                    </div>
                    <div className="flex-1">
                        <label htmlFor="last-name" className="block text-sm font-medium text-gray-700">Last Name</label>
                        <Input
                            type="text"
                            id="last-name"
                            value={form.lastName}
                            onChange={(e) => handleChange("lastName", e.target.value)}
                            required
                        />
                    </div>
                </div>

                <div>
                    <label htmlFor="email" className="block text-sm font-medium text-gray-700">Email</label>
                    <Input
                        type="email"
                        id="email"
                        value={form.email}
                        onChange={(e) => handleChange("email", e.target.value)}
                        required
                    />
                </div>

                <div className="flex gap-4">
                    <div className="flex-1">
                        <label htmlFor="password" className="block text-sm font-medium text-gray-700">Password</label>
                        <Input
                            type="password"
                            id="password"
                            value={form.password}
                            onChange={(e) => handleChange("password", e.target.value)}
                            required
                        />
                    </div>
                    <div className="flex-1">
                        <label htmlFor="confirm-password" className="block text-sm font-medium text-gray-700">Confirm Password</label>
                        <Input
                            type="password"
                            id="confirm-password"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            required
                        />
                    </div>
                </div>

                <Button type="submit" className="w-full" disabled={loading}>
                    {loading ? "Signing Up..." : "Sign Up"}
                </Button>

                <Button type="button" variant="ghost" className="w-full mt-2" onClick={onSwitch}>
                    Already have an account? Log In
                </Button>
            </form>
        </div>
    );
}