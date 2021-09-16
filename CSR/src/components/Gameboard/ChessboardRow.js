import React, { Component } from 'react'
import './ChessboardRow.css'
// import imgN1 from "./../../assets/chessboard/-1.png";
// import img0 from "./../../assets/chessboard/0.png";
// import img1 from "./../../assets/chessboard/1.png";
// import img2 from "./../../assets/chessboard/2.png";
// import img3 from "./../../assets/chessboard/3.png";
// import img4 from "./../../assets/chessboard/4.png";
// import img5 from "./../../assets/chessboard/5.png";
// import img6 from "./../../assets/chessboard/6.png";
// import img7 from "./../../assets/chessboard/7.png";
// import img8 from "./../../assets/chessboard/8.png";
// import img9 from "./../../assets/chessboard/9.png";
// import img10 from "./../../assets/chessboard/10.png";
// import img11 from "./../../assets/chessboard/11.png";
// import img12 from "./../../assets/chessboard/12.png";
// import img13 from "./../../assets/chessboard/13.png";
// import img14 from "./../../assets/chessboard/14.png";
// import img15 from "./../../assets/chessboard/15.png";
// import img16 from "./../../assets/chessboard/16.png";
// import img17 from "./../../assets/chessboard/17.png";
// import img18 from "./../../assets/chessboard/18.png";
// import img19 from "./../../assets/chessboard/19.png";
// import img20 from "./../../assets/chessboard/20.png";
// import img21 from "./../../assets/chessboard/21.png";
// import img22 from "./../../assets/chessboard/22.png";
// import img23 from "./../../assets/chessboard/23.png";
// import img24 from "./../../assets/chessboard/24.png";
// import img25 from "./../../assets/chessboard/25.png";
// import img26 from "./../../assets/chessboard/26.png";
// import img27 from "./../../assets/chessboard/27.png";
// import img28 from "./../../assets/chessboard/28.png";
// import img29 from "./../../assets/chessboard/29.png";
// import img30 from "./../../assets/chessboard/30.png";
// import img31 from "./../../assets/chessboard/31.png";
// import img32 from "./../../assets/chessboard/32.png";
// import img33 from "./../../assets/chessboard/33.png";
// import img34 from "./../../assets/chessboard/34.png";
// import img35 from "./../../assets/chessboard/35.png";
// import img36 from "./../../assets/chessboard/36.png";
// import img37 from "./../../assets/chessboard/37.png";
// import img38 from "./../../assets/chessboard/38.png";
// import img39 from "./../../assets/chessboard/39.png";

export default class ChessboardRow extends Component {

    render() {
        const {cols} = this.props

        return (
            <div className='chessboardRow'>
                {
                    cols.map((col, index)=>(<img alt='chessboardUnit' className='chessboardUnit' key={index} src={require(`./../../assets/chessboard/${col}.png`).default} />))
                }
            </div>
        )
    }
}
