import '../../styles/auth.css'
import { AuthButton } from '../ui/button'

export function CommonUserSignup () {
    return (
        <div className='auth-container'>
            <form className='form-fields'>
                <div className='form-field'>
                    <label className='field-name'>Full Name</label>
                    <input className='input' type='text' />
                </div>
                <div className='form-field'>
                    <label className='field-name'>Username</label>
                    <input className='input' type='text' />
                </div>
                <div className='form-field'>
                    <label className='field-name'>Email</label>
                    <input className='input' type='text' />
                </div>
                <div className='form-field'>
                    <label className='field-name'>Password</label>
                    <input className='input' type='text' />
                </div>
                <div className='form-field'>
                    <label className='field-name'>Confirm Password</label>
                    <input className='input' type='text' />
                </div>
                <div className='action-text'>
                    Want to manage your health better ?
                </div>
                <div className='auth-button'><AuthButton buttonlabel='Signup' onclick={() => {}} /></div>
            </form>
        </div>
    )
}

export function AppAdminSignup () {
    return (
        <div>App Admin Signup</div>
    )
}

export function OrgSignup () {
    return (
        <div>Organization Signup For Admin and Staff</div>
    )
}
