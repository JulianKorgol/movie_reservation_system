import {User} from "@/models/user.model";
import {Role} from "@/models/role.model";

export interface Account {
    id: string;
    user: User;
    role: Role;
    firstName: string;
    lastName: string;
    status?: number;
}