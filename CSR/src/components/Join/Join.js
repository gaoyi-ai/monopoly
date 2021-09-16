import './Join.css'
import React, { Component, createRef } from 'react'
import hostAvatar from "./../../assets/img/default_avatar.png"
import player1 from "./../../assets/img/default_avatar.png"
import player2 from "./../../assets/img/player_2_mark.png"
export default class Join extends Component {
    gameLink = createRef();

    state = {
        players: [player1 ]//, player2
    }

    copyToClipBoard = () => {
        this.gameLink.current.select();
        // window.clipboardData.setData('text', clipBoardContent);
        document.execCommand('copy');
        alert('Game Link Copied');
    }
    render() {
        return (

            <div className='join'>
                {<img className='host_avatar' src={hostAvatar} alt="Host Avatar" />}
                <div className='pannel'>
                    <h2>New Game!</h2>
                    <div className='players'>
                        {this.state.players.map((p, index) => (<img src={p} key={index} alt={`player_${index}`} />))}
                    </div>
                    {(this.state.players.length > 1) ? <button className='startGame' onClick={() =>this.props.history.replace('/gameboard')}>Start Game</button> : <span className='waitHint'>Waiting for friends to join...</span>}

                    <br />
                    <br />
                    <span className='avatarHint'>Let your friends recognize you with a profile photo!</span>
                    <hr></hr>
                    <br />
                    <span className='inviteHint'>Invite your friends to join the game by sharing the link.</span>
                    <br />
                    <input readOnly ref={this.gameLink} value='127.00.0.1:8000/join/admin'></input><button onClick={this.copyToClipBoard} className='inlineButton'>Copy</button>
                </div>
            </div>
        )
    }
}
