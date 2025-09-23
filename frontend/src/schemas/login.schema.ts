import { z } from 'zod';

export const loginSchema = z.object({
    email: z.email("Invalid email address"),
    password: z.string().min(8, "Password is required"),
});

export type LoginSchema = z.infer<typeof loginSchema>;