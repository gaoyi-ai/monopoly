import React, { Component } from 'react';
import { withRouter } from 'react-router';
import { Link } from 'react-router-dom';
import './Login.css';

class Login extends Component {

    usernameRef = React.createRef();
    passwordRef = React.createRef();

    commitData = () => {
        const { value: username } = this.usernameRef.current;
        const { value: password } = this.passwordRef.current;
        if (username && password) {
            if ((password === '123456') && (username === 'admin')) {
                // console.log(`PasswordUsernameComfirmed`);
                this.props.history.replace('/join');
            }
            // console.log(username, password);
        } else if (!username) {
            alert('Please input username');
        } else {
            alert('Please input or check password')
        }
    }



    render() {
        return (
            <div className='Login' key={this.props.location.key}>
                <div className='pannel'>
                    <h2>Login To Monopoly</h2>
                    <input placeholder='User Name' type='text' ref={this.usernameRef}></input>
                    <br />
                    <br />
                    <input placeholder='Password' type='password' ref={this.passwordRef}></input>
                    <br />
                    <br />
                    <button className='bigButton' onClick={this.commitData}>Login</button>
                    <br />
                    <br />
                    <div className='registHint'>
                        <span>New Here? </span><Link to='/register'>Create New Account</Link>
                    </div>
                </div>
            </div>
        )
    }
}

export default withRouter(Login)
