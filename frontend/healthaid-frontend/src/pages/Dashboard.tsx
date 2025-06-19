import { useUser } from "../context/UserContext";
import { UserType, OrgRole } from "../context/userRoles";
import StaffDashboard from "../components/userDashboards/staffdashboard";
import AdminDashoard from "../components/userDashboards/admindashboard";
import OrgDashboard from "../components/userDashboards/orgdashboard";
import CommonUserDashboard from "../components/userDashboards/commonuserdashboard";

const Dashboard = () => {
  const { userType, orgRole } = useUser();

    if (userType === UserType.ADMIN) return <AdminDashoard />;
    if (userType === UserType.USER) return <CommonUserDashboard/>;
    if (userType === UserType.ORGANIZATION) {
        if (orgRole === OrgRole.ORG_ADMIN) {
            return <OrgDashboard />;
        }
        return <StaffDashboard />;
    }
    return <CommonUserDashboard />;
};

export default Dashboard;