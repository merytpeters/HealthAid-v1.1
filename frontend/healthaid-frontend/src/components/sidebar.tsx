import CommonUserSidebar from "./userSidebars/commonuserSidebar";
import StaffSidebar from "./userSidebars/staffsidebar";
import AdminSidebar from "./userSidebars/adminsidebar";
import OrgSidebar from "./userSidebars/orgsidebar";
import { useUser } from "../context/UserContext";
import { UserType, OrgRole } from "../context/userRoles";

const Sidebar = ({ onClose }: { onClose: () => void }) => {
    const { userType, orgRole } = useUser();

    if (import.meta.env.DEV) {
    // Hardcode the sidebar to test in dev mode:
    // return <AdminSidebar />;
    return <CommonUserSidebar onClose={onClose}/>;
    // return <StaffSidebar />;
    // return <OrgSidebar />;
  }

    if (userType === UserType.ADMIN) return <AdminSidebar />;
    if (userType === UserType.USER) return <CommonUserSidebar onClose={onClose}/>;
    if (userType === UserType.ORGANIZATION) {
        if (orgRole === OrgRole.ORG_ADMIN) {
            return <OrgSidebar onClose={onClose}/>;
        }
        return <StaffSidebar onClose={onClose}/>;
    }
    return <CommonUserSidebar onClose={onClose}/>;
};

export default Sidebar;
