import React, { Component } from 'react'

import ChessboardRow from './ChessboardRow';
import './Gameboard.css'
import PlayerState from './PlayerState';
import player0_avatar from './../../assets/img/player_0_mark.png'
import player1_avatar from './../../assets/img/player_1_mark.png'
import player2_avatar from './../../assets/img/player_2_mark.png'

export default class Gameboard extends Component {
    state = {
        diceNumber: 2,
        gameboard: [
            [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
            [19, -1, -1, -1, -1, -1, -1, -1, -1, -1, 31],
            [18, -1, -1, -1, -1, -1, -1, -1, -1, -1, 32],
            [17, -1, -1, -1, -1, -1, -1, -1, -1, -1, 33],
            [16, -1, -1, -1, -1, -1, -1, -1, -1, -1, 34],
            [15, -1, -1, -1, -1, -1, -1, -1, -1, -1, 35],
            [14, -1, -1, -1, -1, -1, -1, -1, -1, -1, 36],
            [13, -1, -1, -1, -1, -1, -1, -1, -1, -1, 37],
            [12, -1, -1, -1, -1, -1, -1, -1, -1, -1, 38],
            [11, -1, -1, -1, -1, -1, -1, -1, -1, -1, 39],
            [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        ],
        isPlaying: true,
        showHint: false,
        players: [
            {
                username: 'alice',
                avatar: player0_avatar,
                cash: 1500,
                x: 600,
                y: 600

            },
            {
                username: 'bill',
                avatar: player2_avatar,
                cash: 1500,
                x: 600,
                y: 600
            },
            {
                username: 'charlie',
                avatar: player1_avatar,
                cash: 1500,
                x: 600,
                y: 600
            }
        ]
    }


    componentDidMount() {
        document.getElementById('bgm').play();
    }

    musicSwitch = () => {
        const { isPlaying } = this.state;
        if (!isPlaying) {
            document.getElementById('bgm').play();
        } else {
            document.getElementById('bgm').pause();
        }
        this.setState({ isPlaying: !isPlaying });
    }

    handleShowHint = () => {
        const { showHint } = this.state;
        this.setState({ showHint: !showHint });
    }

    exitGame = () => {
        let isExit = window.confirm('Exit game?');
        if (isExit) {
            this.props.history.replace('/');
        }
    }

    rollDiceSimulate = () =>{
        if (this.state.diceNumber=2){
            this.setState( {diceNumber:10} );
        }     
    }

    render() {
        return (
            <div className='gameboard'>
                <div className='iconsLeft'>
                    <img src={this.state.isPlaying ? require(`./../../assets/img/musicOn.png`).default : require(`./../../assets/img/musicOff.png`).default} onClick={this.musicSwitch} alt='musicSwitch'></img>
                    <img src={require(`./../../assets/img/help.png`).default} onClick={this.handleShowHint} alt='helpIcon'></img>
                    <img src={require(`./../../assets/img/exit.png`).default} onClick={this.exitGame} alt='exitIcon'></img>
                </div>
                <audio loop='loop' id="bgm" src={require('./../../assets/audio/background.mp3').default}></audio>
                <div className='baseplate'>

                    {this.state.gameboard.map((row, index) => (<ChessboardRow key={index} cols={row} />))}
                    {this.state.players.map((player, index) => (<img alt='' className='token' key={index} src={player.avatar} style={{ left: player.x, top: player.y }} />))}
                    <div className='diceBox'>
                        <img className='dice' alt='dice' src={require(`./../../assets/dice/5dice.png`).default} />
                        <img className='dice' alt='dice' src={require(`./../../assets/dice/3dice.png`).default} />
                        <br />
                        <br />
                        <button className='bigButton' onClick={this.rollDiceSimulate}>Roll Dice!</button>
                        <br />
                        {this.state.players[0].username} got {this.state.diceNumber}!
                    </div>
                </div>

                <div className='iconRight'>  {/* 显示本局游戏玩家状态*/}
                    {this.state.players.map(
                        (player, index) => {
                            return (<PlayerState username={player.username[0]} avatar={player.avatar} cash={player.cash} key={index} />)
                        }
                    )
                    }
                </div>

                {this.state.showHint ? (<div className='hint'  >
                    <div className='construction'>
                        <h2>Construction</h2>
                        <p>When you stop onto a <b>new</b> land, oyu can</p>
                        <ul>
                            <li>do nothing</li>
                            <li>buy the land</li>
                            <li>build a house for $100 (up to three, one at a time</li>
                            <li>upgrade to a hotel for $150</li>
                        </ul>
                        <p>You can also buy infrastructures like Entyopy+, City Grill...</p>
                    </div>
                    <div className='rent'>
                        <h2>Rent</h2>
                        <p>When other players stop onto your land, you will get rent from the player:</p>
                        <ul>
                            <li>1/4 (house) or 1/2 (hotel) of the land price,</li>
                            <li>and $10 for each house,</li>
                            <li>and $50 for the hotel.</li>
                        </ul>
                    </div>
                    <div className='gameProcess'>
                        <h2>Game Process</h2>
                        <ul>
                            <li>You will be suspended for one round if you reach the AIV jail.</li>
                            <li>The game ends after the first player runs out of cash.</li>
                        </ul>
                    </div>
                </div>) : null
                }
            </div>
        )
    }
}