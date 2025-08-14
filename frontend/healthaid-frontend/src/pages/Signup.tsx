import { useUser } from "../context/UserContext";
import { UserType } from "../context/userRoles";
import {
  CommonUserSignup,
  AppAdminSignup,
  OrgSignup
} from "../components/auth/AllSignup";

const Signup = () => {
  const { userType } = useUser();

  if (import.meta.env.Dev) {
    return <CommonUserSignup />
  }

  if (userType === UserType.ADMIN) return <AppAdminSignup />;
  if (userType === UserType.USER) return <CommonUserSignup />;
  if (userType === UserType.ORGANIZATION) return <OrgSignup />;
}

export default Signup;
