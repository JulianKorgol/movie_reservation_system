"use client";
import { useState } from "react";
import LoginForm from "@/app/auth/login-form";
import SignUpForm from "@/app/auth/sign-up-form";

export default function AuthPage() {
    const [showLogin, setShowLogin] = useState(true);

    return (
        <>
            {showLogin ? (
                <LoginForm onSwitch={() => setShowLogin(false)} />
            ) : (
                <SignUpForm onSwitch={() => setShowLogin(true)} />
            )}
        </>
    );
}