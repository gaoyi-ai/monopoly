import React, { Component } from 'react'
import './PlayerState.css'

export default class PlayerState extends Component {
    render() {
        const {username, avatar, cash} = this.props;
        return (
            <div className='playerStateBar'>
                <span className='usernameInitial'>{username}</span>
                <img src={avatar} />
                <span className='cash'>${cash}</span>
            </div>
        )
    }
}
