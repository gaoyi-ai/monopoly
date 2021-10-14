'use strict';

class AI {
    constructor(username, avatar, type = "P", index) {
        this.username = username
        if (avatar.indexOf("media") === -1) {
            this.avatar = "/media/default_avatar.png"
        } else {
            this.avatar = avatar
        }
        this.type = type
        this.index = index;
    }

    isPossible() {
        let random = Math.floor((Math.random() * 10) + 1);
        return random > 5
    }


}