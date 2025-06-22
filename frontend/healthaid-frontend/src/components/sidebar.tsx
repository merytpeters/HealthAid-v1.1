import CommonUserSidebar from "./userSidebars/commonuserSidebar";
import StaffSidebar from "./userSidebars/staffsidebar";
import AdminSidebar from "./userSidebars/adminsidebar";
import OrgSidebar from "./userSidebars/orgsidebar";
import { useUser } from "../context/UserContext";
import { UserType, OrgRole } from "../context/userRoles";

const Sidebar = () => {
    const { userType, orgRole } = useUser();

    if (import.meta.env.DEV) {
    // Hardcode the sidebar to test in dev mode:
    // return <AdminSidebar />;
    return <CommonUserSidebar />;
    // return <StaffSidebar />;
    // return <OrgSidebar />;
  }

    if (userType === UserType.ADMIN) return <AdminSidebar />;
    if (userType === UserType.USER) return <CommonUserSidebar />;
    if (userType === UserType.ORGANIZATION) {
        if (orgRole === OrgRole.ORG_ADMIN) {
            return <OrgSidebar />;
        }
        return <StaffSidebar />;
    }
    return <CommonUserSidebar />;
};

export default Sidebar;
