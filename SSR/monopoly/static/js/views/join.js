"use strict";


class JoinView {
    constructor() {
        this.userName = document.getElementById("user-name").value;
        this.hostName = document.getElementById("host-name").value;
        this.avatar = document.getElementById("user-avatar").getAttribute("src")
        if (this.avatar.indexOf("media") === -1) {
            document.getElementById("user-avatar").src = "/media/default_avatar.png"
        }
        this.friends = new Set();

        this.initComponents();
        this.initWebSocket();
    }

    initComponents() {
        this.$showLobby = false
        this.lobbyUpdate = null;
        this.$enterLobby = document.getElementById("enterLobby")
        this.$enterLobby.addEventListener("click", () => {
            this.showLobby();
        })
        this.$onlineRoomsContainer = document.getElementById("online-rooms-container")
        this.$rooms = document.getElementById("rooms")
        this.$usersContainer = document.getElementById("joined-users-container");
        this.$newGameNotice = document.getElementById("new-game-notice");
        this.$startGame = document.getElementById("start-game");
        this.$startGame.addEventListener("click", () => {
            this.startGame();
        });
        this.$addAI = document.getElementById("add-bots");

        if (this.userName === this.hostName) {
            this.$addAI.classList.remove("hidden")
            this.$addAI.addEventListener("click", () => {
                this.addAI();
            })
            this.$invitationLink = document.getElementById("invitation-url");
            this.$invitationLink.value = `${window.location.host}/monopoly/join/${this.hostName}`;

            this.$copyTooltip = document.getElementById("copied-tooltip");
            this.$copyButton = document.getElementById("share-invitation");
            this.$copyButton.addEventListener("click", () => {
                this.copyToClipboard();
            })
        }

        const isProfileInited = this.avatar.length !== 0;
        if (!isProfileInited) {
            const $addProfileButton = document.getElementById("init-profile");
            $addProfileButton.classList.remove("hidden");
        }
    }

    initWebSocket() {
        this.socket = new WebSocket(`ws://${window.location.host}/ws/join/${this.hostName}/?player=${this.userName}`);

        const socket = this.socket;
        const openMsg = {
            action: "join",
            type: 0
        };

        // Connection opened
        this.socket.addEventListener('open', function (event) {
            socket.send(JSON.stringify(openMsg));
        });


        this.socket.onmessage = (event) => {
            const message = JSON.parse(event.data);
            this.handleStatusChange(message);
        }

        const refreshMsg = {
            action: "refresh"
        };

        setInterval(() => {
            socket.send(JSON.stringify(refreshMsg))
        }, 5000)
    }

    handleStatusChange(message) {
        if (message.action === "join") {
            this.addFriend(message.data);
            if (this.userName === this.hostName) {
                this.canAddAI();
            }

            if (this.friends.size > 0) {
                if (this.hostName !== this.userName) {
                    this.$startGame.innerText = "Waiting for host to start the game...";
                } else {
                    this.$startGame.disabled = false;
                    this.$startGame.innerText = "Start Game";
                }
            }
        } else if (message.action === "start") {
            this.navigateToGame();
        } else if (message.action === "fail_join") {
            this.$startGame.disabled = true;
            this.$startGame.innerText = "Navigating back... Create your own game";
            if (message.data === 0) {
                this.$newGameNotice.innerText = "4 Players Max Per Game!";
            } else {  // message.data === 1
                this.$newGameNotice.innerText = "Room Not Exists... Maybe host disbanded this room";
            }
            this.$newGameNotice.style.color = "#F44336";
            setTimeout(this.navigateBack, 3000);
        }
    }

    addFriend(friends) {
        this.friends.clear()
        this.$usersContainer.innerHTML = '';
        for (let friend of friends) {
            // if (this.friends.indexOf(friend.name) !== -1 || friend.name === this.userName) continue;
            // if (!this.friends.prototype.includes(friend.name)) {
            this.friends.add(friend.name);
            if (friend.avatar.indexOf("media") === -1) {
                friend.avatar = "/media/default_avatar.png"
            }

            this.$usersContainer.innerHTML += `
                <a href="/monopoly/profile/${friend.name}" target="_blank">
                    <img class="joined-user-avatar" src="${friend.avatar}" title="${friend.name}">
                </a>
            `;
        }
        console.log(this.friends)
    }

    canAddAI() {
        if (!this.friends.has("AI") && this.friends.size > 0 && this.friends.size < 4) {
            this.$addAI.innerText = "Want to add AI bots...";
            this.$addAI.disabled = false;
        } else {
            this.$addAI.disabled = true;
        }
    }

    showLobby() {
        this.$showLobby = !this.$showLobby
        console.log(this.$showLobby)
        this.$onlineRoomsContainer.style.visibility = "visible"
        const msg = {
            action: "query",
        };
        if (this.lobbyUpdate === null) {
            this.socket2 = new WebSocket(`ws://${window.location.host}/ws/lobby/`);
            this.socket2.addEventListener("open", () => {
                this.lobbyUpdate = setInterval(() => this.socket2.send(JSON.stringify(msg)), 2000);
            })
            this.socket2.onmessage = (event) => {
                const message = JSON.parse(event.data);
                this.handleLobbyChange(message);
            }
        }
        if (!this.$showLobby) {
            this.$onlineRoomsContainer.style.visibility = "hidden"
            clearInterval(this.lobbyUpdate)
            this.lobbyUpdate = null
        }
    }

    handleLobbyChange(msg) {
        const {lobby} = msg
        this.lobby = lobby
        this.$rooms.innerHTML = '';

        for (let room of lobby) {
            let host = room.host
            let players = room.players
            let status = room.status
            if (status !== "WAITING" || host === this.userName) {
                this.$rooms.innerHTML += `
            <div id="room-${host}">
                <span>Room Host: </span>
                <button disabled>${host}</button>
                <div id="room-${host}-status">State: ${status}</div>
                <span>Players: </span>
                <span>${players}</span>
            </div>
            `;
            } else {
                this.$rooms.innerHTML += `
            <div id="room-${host}">
                <span>Room Host: </span>
                <button class="light-button">${host}</button>
                <div id="room-${host}-status">State: ${status}</div>
                <span>Players: </span>
                <span>${players}</span>
            </div>
            `;
            }
        }
        let roomDoor = document.querySelectorAll("[id^='room-'] > button")
        roomDoor.forEach(btn => btn.addEventListener("click", () => {
            window.location = `http://${window.location.host}/monopoly/join/${btn.innerHTML}`;
        }))

    }

    addAI() {
        const msg = {
            action: "join",
            type: 1
        };
        this.socket.send(JSON.stringify(msg))
    }

    startGame() {
        this.socket.send(JSON.stringify({
            action: "start"
        }));
    }

    navigateToGame() {
        window.location = `http://${window.location.host}/monopoly/game/${this.hostName}`;
    }

    navigateBack() {
        window.location = `http://${window.location.host}/monopoly`;
    }

    copyToClipboard() {
        let copyText = this.$invitationLink;
        copyText.select();
        document.execCommand("Copy");

        this.$copyTooltip.classList.add("shown");
        setTimeout(() => {
            this.$copyTooltip.classList.remove("shown");
        }, 2000);
    }
}

window.onload = () => {
    new JoinView();
};