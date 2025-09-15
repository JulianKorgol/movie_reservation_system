export interface User {
    id: string;
    email: string;
    firstName: string;
    lastName: string;
    password_hash?: string;
    password_date_change?: Date;
    role: "user" | "admin";
    status?: "active" | "inactive" | "banned";
    createdAt?: Date;
    updatedAt?: Date;
}