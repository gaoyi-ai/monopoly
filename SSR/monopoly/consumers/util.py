from channels.db import database_sync_to_async
from django.contrib.auth.models import User

from monopoly.models import Profile

rooms = {}
games = {}
change_handlers = {}
decisions = {}
readys = {}


@database_sync_to_async
def get_user(player):
    return User.objects.get(username=player)


@database_sync_to_async
def get_profile(user):
    return Profile.objects.get(user=user)


async def build_init_msg(players, cash_change, pos_change, wait_decision, decision, next_player,
                         title, landname, owners, houses):
    players_list = []
    for player in players:
        user = await get_user(player)
        profile = await get_profile(user)
        avatar = profile.avatar.url if profile.avatar.name else ""
        players_list.append({"fullName": user.username,
                             "userName": user.username,
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


def build_buy_land_msg(curr_player, curr_cash, tile_id, next_player):
    ret = {"action": "buy_land",
           "curr_player": curr_player,
           "curr_cash": curr_cash,
           "tile_id": tile_id,
           "next_player": next_player,
           }
    return ret


def build_construct_msg(curr_cash, tile_id, build_type, next_player):
    ret = {"action": "construct",
           "curr_cash": curr_cash,
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
