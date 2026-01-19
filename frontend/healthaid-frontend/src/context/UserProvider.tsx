import { useState, type ReactNode } from "react";
import { UserContext } from "./UserContext";
import { UserType, type OrgRole } from "./userRoles";

export type UserContextType = {
  userType: UserType;
  orgRole?: OrgRole | null;
  setUserType: (type: UserType) => void;
  setOrgRole: (role: OrgRole | null) => void;
};

export const UserProvider = ({ children }: { children: ReactNode }) => {
  const [userType, setUserType] = useState<UserType>(UserType.USER);
  const [orgRole, setOrgRole] = useState<OrgRole | null>(null);

  return (
    <UserContext.Provider value={{ userType, orgRole, setUserType, setOrgRole }}>
      {children}
    </UserContext.Provider>
  );
};
