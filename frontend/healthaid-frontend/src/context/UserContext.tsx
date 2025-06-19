import { createContext, useContext, useState } from "react";
import type { ReactNode } from "react";
import { UserType, OrgRole } from "./userRoles";

type UserContextType = {
  userType: UserType;
  orgRole?: OrgRole | null;
  setUserType: (type: UserType) => void;
  setOrgRole: (role: OrgRole | null) => void;
};

const UserContext = createContext<UserContextType | undefined>(undefined);

export const UserProvider = ({ children }: { children: ReactNode }) => {
  // Default userType is 'user' for development purposes
  const [userType, setUserType] = useState<UserType>(UserType.USER);

  // orgRole is null unless userType is 'organization'
  const [orgRole, setOrgRole] = useState<OrgRole | null>(null);

  return (
    <UserContext.Provider value={{ userType, orgRole, setUserType, setOrgRole }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = (): UserContextType => {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error("useUser must be used within a UserProvider");
  }
  return context;
};
