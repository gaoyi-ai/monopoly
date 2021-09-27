from monopoly.consumers.message import build_roll_res_msg, build_game_end_msg, build_buy_land_msg, build_construct_msg, \
    build_cancel_decision_msg, build_chat_msg
from monopoly.consumers.util import games, rooms, decisions, readys
from monopoly.core.game import Game
from monopoly.core.land import LandType, Land, BuildingType
from monopoly.core.move_receipt import MoveReceiptType, ModalTitleType, MoveReceipt
from monopoly.handlers.notice_handler import NoticeHandler


def handle_ready(**kwargs):
    h = kwargs['h']
    player = kwargs['player']
    if h not in readys:
        readys[h] = set()
    readys[h].add(player)
    if "AI" in rooms[h].players:
        readys[h].add("AI")

    if len(rooms[h]) == len(readys[h]):
        return True
    return False


async def handle_roll(**kwargs):
    h = kwargs['h']
    gs = kwargs['gs']
    chs = kwargs['chs']
    game = gs[h]
    players = game.players
    move_receipt: MoveReceipt
    steps, move_receipt = game.roll()
    cur_player_ind = game.cur_player.index
    new_pos = game.cur_player.position
    is_option = "false"
    is_cash_change = "false"
    new_event = "true"
    curr_cash = []
    next_player_ind = None
    bypass_start = None
    change_handler: NoticeHandler = chs[h]

    if move_receipt.type in [MoveReceiptType.CONSTRUCTION_OPTION, MoveReceiptType.BUY_LAND_OPTION]:
        decisions[h] = move_receipt
        is_option = "true"
    elif move_receipt.type in [MoveReceiptType.PAYMENT, MoveReceiptType.REWARD]:
        game.execute_move_receipt(move_receipt)
        next_player_ind = game.cur_player.index
        is_cash_change = "true"
        curr_cash = [player.money for player in players]
    elif move_receipt.type == MoveReceiptType.NOTHING:
        game.execute_move_receipt(move_receipt)
        next_player_ind = game.cur_player.index
        new_event = "false"
    else:  # MoveReceiptType.STOP_ROUND
        game.execute_move_receipt(move_receipt)
        next_player_ind = game.cur_player.index

    if is_option == "false" and change_handler.game_end:  # non-option and game end
        all_asset = [player.assets_evaluation() for player in players]
        msg = build_game_end_msg(cur_player_ind, all_asset)
        return msg

    title = ModalTitleType.description(move_receipt.type)
    landname = move_receipt.land.description

    if change_handler.is_bypass_start:
        bypass_start = "true"
        change_handler.is_bypass_start = False
        curr_cash = [player.money for player in players]

    msg = build_roll_res_msg(cur_player_ind, steps, move_receipt.beautify(), is_option, is_cash_change,
                             new_event, new_pos, curr_cash, next_player_ind, title, landname, bypass_start)
    return msg


async def handle_end_game(**kwargs):
    h = kwargs['h']
    gs = kwargs['gs']
    if gs.get(h) is None:
        return
    game = gs[h]
    players = game.players
    all_asset = [player.assets_evaluation() for player in players]
    curr_player_ind = game.cur_player.index
    msg = build_game_end_msg(curr_player_ind, all_asset)

    if decisions.get(h): decisions.pop(h)
    games.pop(h)
    if rooms.get(h): rooms.pop(h)
    return msg


async def handle_confirm_decision(**kwargs):
    h = kwargs['h']
    gs = kwargs['gs']
    game = gs[h]
    cur_player = game.cur_player.index
    if h not in decisions:
        return
    decision: MoveReceipt = decisions.pop(h)
    decision.option = True
    confirm_result: MoveReceipt = game.execute_move_receipt(decision)
    players = game.players
    cur_cash = [player.money for player in players]
    next_player_idx = game.cur_player.index

    if confirm_result.type == MoveReceiptType.BUY_LAND_OPTION:
        tile_id = confirm_result.land.pos
        msg = build_buy_land_msg(cur_player, cur_cash, tile_id, next_player_idx)
    elif confirm_result.type == MoveReceiptType.CONSTRUCTION_OPTION:
        tile_id = confirm_result.land.pos
        build_type = "house" if confirm_result.land.content.property_type == BuildingType.HOUSE else "hotel"
        msg = build_construct_msg(cur_player, cur_cash, tile_id, build_type, next_player_idx)
    else:  # MoveReceiptType.NOTHING
        msg = build_cancel_decision_msg(cur_player, next_player_idx, "no enough money")
    return msg


async def handle_cancel_decision(**kwargs):
    h = kwargs['h']
    gs = kwargs['gs']
    game = gs[h]
    if h not in decisions:
        return
    cur_player_ind = game.cur_player.index
    decision: MoveReceipt = decisions.pop(h)
    decision.option = False
    game.execute_move_receipt(decision)
    next_player_ind = game.cur_player.index
    msg = build_cancel_decision_msg(cur_player_ind, next_player_ind)
    return msg


async def handle_chat(**kwargs):
    message = kwargs['message']
    sender = message["from"]
    content = message["content"]
    msg = build_chat_msg(sender, content)
    return msg


def get_building_type(tile_id, game: Game):
    land: Land = game._board.land_at(tile_id)
    if land.content.type == LandType.CONSTRUCTABLE:
        building = land.content.property_type
        if building == BuildingType.HOTEL:
            res = 4
        elif building == BuildingType.HOUSE:
            res = land.content.building_num
        else:
            res = 0
    else:
        res = 0
    return res
