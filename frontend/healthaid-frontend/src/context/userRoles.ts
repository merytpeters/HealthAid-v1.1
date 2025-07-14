export type UserType = "admin" | "user" | "organization";

export const UserType = {
    ADMIN: "admin" as UserType,
    USER: "user" as UserType,
    ORGANIZATION: "organization" as UserType,
};

export type OrgRole = "org_admin" | "doctor" | "nurse" | "staff";

export const OrgRole = {
    ORG_ADMIN: "org_admin" as OrgRole,
    DOCTOR: "doctor" as OrgRole,
    NURSE: "nurse" as OrgRole,
    STAFF: "staff" as OrgRole,
};
