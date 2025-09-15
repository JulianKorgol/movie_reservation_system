'use client';

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { authService } from "@/services/auth.service";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { loginSchema, type LoginSchema } from "@/schemas/login.schema";
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert";
import { AlertCircleIcon } from "lucide-react";
import { useState } from "react";

export default function LoginForm({ onSwitch }: { onSwitch: any }) {
    const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<LoginSchema>({
        resolver: zodResolver(loginSchema),
        mode: "onBlur",
    });

    const [serverErrors, setServerErrors] = useState<string[]>([]);

    const onSubmit = async (data: LoginSchema) => {
        setServerErrors([]);

        try {
            const response = await authService.login(data);
            console.log("Login successful:", response);
            localStorage.setItem("authToken", response.token);
            // TODO: redirect to dashboard or home
        } catch (error) {
            console.error("Login failed:", error);
            setServerErrors(["Invalid email or password."]);
        }
    };

    const allErrors = [
        ...Object.values(errors).map(err => err?.message as string),
        ...serverErrors
    ];

    return (
        <div className="font-sans min-h-screen p-8 pb-20 gap-16 sm:p-20">
            <header>
                <h1 className="text-3xl font-bold text-center mt-10">Log In</h1>
            </header>

            <form
                onSubmit={handleSubmit(onSubmit)}
                className="flex flex-col gap-2 max-w-sm mx-auto mt-20"
                noValidate
            >
                <div>
                    <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                        Email
                    </label>
                    <Input
                        id="email"
                        type="email"
                        {...register("email")}
                        className={errors.email ? "border-red-500 focus:ring-red-500 focus:border-red-500" : ""}
                    />
                </div>

                <div>
                    <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
                        Password
                    </label>
                    <Input
                        id="password"
                        type="password"
                        {...register("password")}
                        className={errors.password ? "border-red-500 focus:ring-red-500 focus:border-red-500" : ""}
                    />
                </div>

                <Button type="submit" className="w-full" disabled={isSubmitting}>
                    {isSubmitting ? "Logging in..." : "Log In"}
                </Button>

                <Button type="button" variant="ghost" className="w-full mt-2" onClick={onSwitch}>
                    Don&apos;t have an account? Sign Up
                </Button>

                {allErrors.length > 0 && (
                    <Alert variant="destructive" className="mt-2 flex items-start gap-2">
                        <AlertCircleIcon className="w-5 h-5 mt-1" />
                        <div>
                            <AlertTitle>Error</AlertTitle>
                            <AlertDescription>
                                {allErrors.map((err, idx) => (
                                    <span key={idx}>
                                        {err}
                                        <br />
                                    </span>
                                ))}
                            </AlertDescription>
                        </div>
                    </Alert>
                )}
            </form>
        </div>
    );
}