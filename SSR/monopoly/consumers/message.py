from monopoly.consumers.util import get_user, get_profile, rooms


async def build_init_msg(players, cash_change, pos_change, wait_decision, decision, next_player,
                         title, landname, owners, houses):
    players_list = []
    for player in players:
        user = await get_user(player)
        profile = await get_profile(user)
        avatar = profile.avatar.url if profile.avatar.name else ""
        players_list.append({"userName": user.username,
                             "avatar": avatar})

    ret = {"action": "init",
           "players": players_list,
           "changeCash": cash_change,
           "posChange": pos_change,
           "waitDecision": wait_decision,
           "decision": decision,
           "nextPlayer": next_player,
           "title": title,
           "landname": landname,
           "owners": owners,
           "houses": houses,
           }
    return ret


def build_add_err_msg():
    ret = {"action": "add_err"}
    return ret


def build_roll_res_msg(curr_player, steps, result, is_option, is_cash_change, new_event,
                       new_pos, curr_cash, next_player, title, landname, bypass_start):
    ret = {"action": "roll_res",
           "curr_player": curr_player,
           "steps": steps,
           "result": result,
           "is_option": is_option,
           "is_cash_change": is_cash_change,
           "new_event": new_event,
           "new_pos": new_pos,
           "curr_cash": curr_cash,
           "next_player": next_player,
           "title": title,
           "landname": landname,
           "bypass_start": bypass_start,
           }
    return ret


def build_game_end_msg(curr_player, all_asset):
    ret = {"action": "game_end",
           "loser": curr_player,
           "all_asset": all_asset}
    return ret


def build_buy_land_msg(cur_player, cur_cash, tile_id, next_player):
    ret = {"action": "buy_land",
           "cur_player": cur_player,
           "cur_cash": cur_cash,
           "tile_id": tile_id,
           "next_player": next_player,
           }
    return ret


def build_construct_msg(cur_player, cur_cash, tile_id, build_type, next_player):
    ret = {"action": "construct",
           "cur_player": cur_player,
           "cur_cash": cur_cash,
           "tile_id": tile_id,
           "build_type": build_type,
           "next_player": next_player,
           }
    return ret


def build_cancel_decision_msg(cur_player, next_player,
                              msg="pass"):
    ret = {"action": "cancel_decision",
           "cur_player": cur_player,
           "next_player": next_player,
           "msg": msg}
    return ret


def build_pass_start_msg(curr_player):
    ret = {"action": "pass_start",
           "curr_player": curr_player,
           }
    return ret


def build_chat_msg(sender, content):
    ret = {"action": "chat",
           "sender": sender,
           "content": content,
           }
    return ret


def build_ready_msg(ready_state):
    ret = {"action": "ready",
           "isReady": ready_state}
    return ret


def build_join_failed_msg(status=0):
    ret = {"action": "fail_join", "data": status}
    return ret


async def generate_room_data(players):
    data = []
    for player in players:
        user = await get_user(player)
        profile = await get_profile(user)
        avatar = profile.avatar.url if profile.avatar.name else ''
        data.append({"name": player, "avatar": avatar})
    return data


async def build_join_reply_msg(room_name):
    players = rooms[room_name].players
    data = await generate_room_data(players)
    ret = {"action": "join", "data": data}
    return ret


def build_start_msg():
    ret = {"action": "start"}
    return ret
