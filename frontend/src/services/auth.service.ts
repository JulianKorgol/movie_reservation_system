import { LoginRequest, SignUpRequest, AuthResponse } from "@/models/auth.model";
import { User } from "@/models/user.model";

export const authService = {
    async login(data: LoginRequest): Promise<AuthResponse> {
        console.log("Mock login request:", data);

        const mockUser: User = {
            id: "1",
            email: data.email,
            firstName: "John",
            lastName: "Doe",
            role: "user",
            status: "active",
            createdAt: new Date(),
            updatedAt: new Date(),
        };

        return new Promise((resolve) =>
            setTimeout(() => resolve({ token: "mock-jwt-token", user: mockUser }), 1000)
        );
    },

    async signUp(data: SignUpRequest): Promise<AuthResponse> {
        console.log("Mock sign-up request:", data);

        const mockUser: User = {
            id: "2",
            email: data.email,
            firstName: data.firstName,
            lastName: data.lastName,
            role: "user",
            status: "active",
            createdAt: new Date(),
            updatedAt: new Date(),
        };

        return new Promise((resolve) =>
            setTimeout(() => resolve({ token: "mock-jwt-token", user: mockUser }), 1000)
        );
    },
};