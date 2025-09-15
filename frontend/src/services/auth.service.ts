import { LoginRequest, SignUpRequest, AuthResponse } from "@/models/auth.model";
import {Account} from "@/models/account.model";
import { User } from "@/models/user.model";
import { Role } from "@/models/role.model";

export const authService = {
    async login(data: LoginRequest): Promise<AuthResponse> {
        console.log("Mock login request:", data);

        const mockUser: User = {
            id: "1",
            username: "johndoe",
            email: data.email,
            password: data.password,
        }

        const mockRole: Role = {
            id: "1",
            name: "admin",
        }

        const mockAccount: Account = {
            id: "1",
            user: mockUser,
            firstName: "John",
            lastName: "Doe",
            role: mockRole,
            status: 1,
        };

        return new Promise((resolve) =>
            setTimeout(() => resolve({ token: "mock-jwt-token", account: mockAccount }), 1000)
        );
    },

    async signUp(data: SignUpRequest): Promise<AuthResponse> {
        console.log("Mock sign-up request:", data);

        const mockUser: User = {
            id: "1",
            username: "johndoe",
            email: data.email,
            password: data.password,
        }

        const mockRole: Role = {
            id: "1",
            name: "admin",
        }

        const mockAccount: Account = {
            id: "1",
            user: mockUser,
            firstName: "John",
            lastName: "Doe",
            role: mockRole,
            status: 1,
        };

        return new Promise((resolve) =>
            setTimeout(() => resolve({ token: "mock-jwt-token", account: mockAccount }), 1000)
        );
    },
};