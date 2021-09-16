import React, { Component } from 'react';
import { withRouter } from 'react-router';
import './Register.css';

class Register extends Component {

    usernameRef = React.createRef();
    passwordRef = React.createRef();
    confirmPasswordRef = React.createRef();

    commitRegisterData = () => {
        const { value: username } = this.usernameRef.current;
        const { value: password } = this.passwordRef.current;
        const { value: confirmPassword } = this.confirmPasswordRef.current;
            // Oops, username occupied!
            // THIS IS FOR SIMULATION
            // 模拟用户名已存在
        if(username === 'admin'){
            alert(`Username "${username}" already existed`);
        }else if (username && password) {
            // brand new username and registed successfully
            // 注册成功
            if (password === confirmPassword) {
                alert('Register Succeeded. Click "OK" to reach login page.');
                this.props.history.replace('/');
            } else {
                alert('The first password you entered mismatch the one for conformation');  // 两次密码不一致
            }
        } else if (!username) {  // username is null 用户名为空
            alert('Please input username');
        } else {
            alert('Please input or check password')  // 未输入密码
        }
    }

    render() {
        return (
            <div className='Login' key={this.props.location.key}>
                <div className='pannel'>
                    <h2>Register</h2>
                    <input placeholder='User Name' type='text' ref={this.usernameRef}></input>
                    <br />
                    <br />
                    <input placeholder='Password' type='password' ref={this.passwordRef}></input>
                    <br />
                    <br />
                    <input placeholder='Confirm Password' type='password' ref={this.confirmPasswordRef}></input>
                    <br />
                    <br />
                    <button className='bigButton' onClick={this.commitRegisterData}>Register</button>
                </div>
            </div >
        )
    }
}
export default withRouter(Register)