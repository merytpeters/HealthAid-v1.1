import '../styles/auth.css'
import { AuthButton } from '../components/ui/button'

function Login () {
  return (
    <div className='auth-container'>
      <form className='form-fields'>
        <div className='login-form-field'>
          <label className='field-name'>Email</label>
          <input className='input' type='text' />
        </div>
        <div className='login-form-field'>
          <label className='field-name'>Password</label>
          <input className='input' type='text' />
        </div>
        <div className='action-text'>
          Forgot Password ?
        </div>
        <div className='auth-button'><AuthButton buttonlabel='Sign in' onclick={() => {}} /></div>
        <div className='line'>or</div>
        <div className='auth-button'><AuthButton buttonlabel='Sign in with Google' onclick={() => {}} /></div>
      </form>
    </div>
  )
}

export default Login