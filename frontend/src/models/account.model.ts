import { User } from "@/models/user.model";
import { Role } from "@/models/role.model";

export interface Account {
  id?: string;
  user: User;
  role: Role;
  first_name?: string | null;
  last_name?: string | null;
  status: 0 | 1 | 2; // 0: banned, 1: active, 2: e-mail not activated
}
