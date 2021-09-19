"use strict";

/**
 *WebSocket Interface
 */

/*const receivedMessage = {
    'action': "join" | "start",
    data: [{
        id: "user_id",
        name: "user_name",
        avatar: "user_url"
    }]
};

const sentMessage = {
    action: "start"
};*/

class JoinView {
    constructor() {
        this.userName = document.getElementById("user-name").value;
        this.hostName = document.getElementById("host-name").value;
        this.avatar = document.getElementById("user-avatar").getAttribute("src")
        if (this.avatar.indexOf("media") === -1) {
            document.getElementById("user-avatar").src = "/media/default_avatar.png"
        }
        this.friends = [this.userName];

        this.initComponents();
        this.initWebSocket();
    }

    initComponents() {
        this.$usersContainer = document.getElementById("joined-users-container");
        this.$newGameNotice = document.getElementById("new-game-notice");
        this.$startGame = document.getElementById("start-game");
        this.$startGame.addEventListener("click", () => {
            this.startGame();
        });

        if (this.userName === this.hostName) {
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
        this.socket = new WebSocket(`ws://${window.location.host}/ws/join/${this.hostName}/`);

        if (this.hostName !== this.userName) {
            const socket = this.socket;
            const openMsg = {
                'action': "join",
                data: [{
                    name: this.userName,
                    avatar: this.avatar
                }]
            };

            // Connection opened
            socket.addEventListener('open', function (event) {
                socket.send(JSON.stringify(openMsg));
            });
        }


        this.socket.onmessage = (event) => {
            const message = JSON.parse(event.data);
            this.handleStatusChange(message);
        }
    }

    handleStatusChange(message) {
        if (message.action === "join") {
            this.addFriend(message.data);

            if (this.friends.length > 1) {
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
            this.$startGame.innerText = "Navigating back... Create your own game!";
            this.$newGameNotice.innerText = "4 Players Max Per Game!";
            this.$newGameNotice.style.color = "#F44336";
            setTimeout(this.navigateBack, 5000);
        }
    }

    addFriend(friends) {
        for (let friend of friends) {
            if (this.friends.indexOf(friend.name) !== -1 || friend.name === this.userName) continue;

            this.friends.push(friend.name);
            if (friend.avatar.indexOf("media") === -1) {
                friend.avatar = "/media/default_avatar.png"
            }

            this.$usersContainer.innerHTML += `
                <a href="/monopoly/profile/${friend.name}" target="_blank">
                    <img class="joined-user-avatar" src="${friend.avatar}" title="${friend.name}">
                </a>
            `;
        }
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