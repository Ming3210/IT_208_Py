# chess.py
# Simple Chess game (local two-player) using pygame
# Features:
# - Complete piece movement rules (except en-passant)
# - Castling (both sides)
# - Pawn promotion (auto promote to Queen)
# - Move legality filtering (no moving into check)
# - Detect check, checkmate, stalemate
# - Click-to-move or drag (click source then click dest)
# - Undo with U, restart with R, quit with Esc
#
# Author: ChatGPT
import pygame
import sys
from copy import deepcopy

# -------- Config ----------
TILE = 80
BOARD_SIZE = 8
WIDTH = TILE * BOARD_SIZE + 250  # extra side panel
HEIGHT = TILE * BOARD_SIZE
FPS = 60

WHITE = (245, 245, 245)
BLACK = (35, 35, 35)
LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)
HIGHLIGHT = (100, 200, 120, 120)
RED = (200, 40, 40)
BLUE = (40, 80, 200)
PANEL_BG = (30, 30, 30)
TEXT_COLOR = (230,230,230)

pygame.init()
FONT = pygame.font.SysFont(None, 20)
BIGFONT = pygame.font.SysFont(None, 28)

# -------- Board representation ----------
# We'll use an 8x8 list of strings. Piece notation:
# White: 'P','N','B','R','Q','K'
# Black: lowercase 'p','n','b','r','q','k'
# Empty: '.'

START_FEN = (
    "rnbqkbnr/"
    "pppppppp/"
    "8/"
    "8/"
    "8/"
    "8/"
    "PPPPPPPP/"
    "RNBQKBNR"
)

def fen_to_board(fen):
    board = [['.' for _ in range(8)] for _ in range(8)]
    rows = fen.split('/')
    for r, row in enumerate(rows):
        c = 0
        for ch in row:
            if ch.isdigit():
                c += int(ch)
            else:
                board[r][c] = ch
                c += 1
    return board

def board_to_fen(board):
    rows = []
    for r in range(8):
        empty = 0
        s = ""
        for c in range(8):
            p = board[r][c]
            if p == '.':
                empty += 1
            else:
                if empty:
                    s += str(empty)
                    empty = 0
                s += p
        if empty:
            s += str(empty)
        rows.append(s)
    return "/".join(rows)

# -------- Utility ----------
def inside(r,c):
    return 0 <= r < 8 and 0 <= c < 8

def is_white(piece):
    return piece.isupper()

def is_black(piece):
    return piece.islower()

def same_color(a,b):
    if a == '.' or b == '.': return False
    return (a.isupper() and b.isupper()) or (a.islower() and b.islower())

# -------- Move generation ----------
# We'll generate pseudo-legal moves then filter out those leaving king in check.
# Move represented as tuple: (sr,sc,tr,tc, promotion_char or None, is_castle (0/1/2))
# is_castle: 0 normal, 1 king-side, 2 queen-side

def find_king(board, white):
    target = 'K' if white else 'k'
    for r in range(8):
        for c in range(8):
            if board[r][c] == target:
                return (r,c)
    return None

def generate_pseudo_moves(board, white_to_move, castling_rights, ep_target):
    moves = []
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if p == '.': continue
            if white_to_move and not p.isupper(): continue
            if not white_to_move and not p.islower(): continue
            piece = p.lower()
            if piece == 'p':
                moves += pawn_moves(board, r, c, white_to_move, ep_target)
            elif piece == 'n':
                moves += knight_moves(board, r, c)
            elif piece == 'b':
                moves += bishop_moves(board, r, c)
            elif piece == 'r':
                moves += rook_moves(board, r, c)
            elif piece == 'q':
                moves += queen_moves(board, r, c)
            elif piece == 'k':
                moves += king_moves(board, r, c, white_to_move, castling_rights)
    return moves

def pawn_moves(board, r, c, white, ep_target):
    moves = []
    dir = -1 if white else 1
    start_row = 6 if white else 1
    promote_row = 0 if white else 7
    opponent = is_black if white else is_white

    # forward 1
    nr, nc = r + dir, c
    if inside(nr,nc) and board[nr][nc] == '.':
        # promotion?
        if nr == promote_row:
            moves.append((r,c,nr,nc,'Q',0))
        else:
            moves.append((r,c,nr,nc,None,0))
        # forward 2
        nr2 = r + 2*dir
        if r == start_row and board[nr2][nc] == '.':
            moves.append((r,c,nr2,nc,None,0))
    # captures
    for dc in (-1,1):
        cr, cc = r + dir, c + dc
        if inside(cr,cc):
            target = board[cr][cc]
            if target != '.' and opponent(target):
                if cr == promote_row:
                    moves.append((r,c,cr,cc,'Q',0))
                else:
                    moves.append((r,c,cr,cc,None,0))
    # en-passant (if ep_target provided as (r,c))
    if ep_target:
        er, ec = ep_target
        if r + dir == er and abs(ec - c) == 1:
            moves.append((r,c,er,ec,None,0))
    return moves

def knight_moves(board, r, c):
    moves = []
    for dr,dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
        nr, nc = r+dr, c+dc
        if inside(nr,nc):
            if board[nr][nc] == '.' or not same_color(board[r][c], board[nr][nc]):
                moves.append((r,c,nr,nc,None,0))
    return moves

def sliding_moves(board, r, c, directions):
    moves = []
    for dr,dc in directions:
        nr, nc = r+dr, c+dc
        while inside(nr,nc):
            if board[nr][nc] == '.':
                moves.append((r,c,nr,nc,None,0))
            else:
                if not same_color(board[r][c], board[nr][nc]):
                    moves.append((r,c,nr,nc,None,0))
                break
            nr += dr; nc += dc
    return moves

def bishop_moves(board, r, c):
    return sliding_moves(board, r, c, [(-1,-1),(-1,1),(1,-1),(1,1)])

def rook_moves(board, r, c):
    return sliding_moves(board, r, c, [(-1,0),(1,0),(0,-1),(0,1)])

def queen_moves(board, r, c):
    return sliding_moves(board, r, c, [(-1,-1),(-1,1),(1,-1),(1,1),(-1,0),(1,0),(0,-1),(0,1)])

def king_moves(board, r, c, white, castling_rights):
    moves = []
    for dr in (-1,0,1):
        for dc in (-1,0,1):
            if dr==0 and dc==0: continue
            nr, nc = r+dr, c+dc
            if inside(nr,nc):
                if board[nr][nc] == '.' or not same_color(board[r][c], board[nr][nc]):
                    moves.append((r,c,nr,nc,None,0))
    # castling: castling_rights is dict: {'K':bool,'Q':bool,'k':bool,'q':bool}
    # King must not be in check, squares traversed must be empty and not attacked.
    # We'll mark is_castle 1 for king-side, 2 for queen-side.
    if white:
        if castling_rights.get('K',False):
            # squares f1 (r,5) and g1 (r,6) must be empty, not attacked
            if board[7][5]=='.' and board[7][6]=='.':
                moves.append((r,c,7,6,None,1))
        if castling_rights.get('Q',False):
            if board[7][1]=='.' and board[7][2]=='.' and board[7][3]=='.':
                moves.append((r,c,7,2,None,2))
    else:
        if castling_rights.get('k',False):
            if board[0][5]=='.' and board[0][6]=='.':
                moves.append((r,c,0,6,None,1))
        if castling_rights.get('q',False):
            if board[0][1]=='.' and board[0][2]=='.' and board[0][3]=='.':
                moves.append((r,c,0,2,None,2))
    return moves

# -------- Make and unmake moves (returns new state) ----------
def make_move(state, move):
    # state is dict: board, white_to_move, castling_rights (dict), ep_target (r,c or None), halfmove, fullmove
    board = deepcopy(state['board'])
    sr,sc,tr,tc,prom,castle = move
    piece = board[sr][sc]
    captured = board[tr][tc]
    board[sr][sc] = '.'
    board[tr][tc] = piece
    # pawn double move sets ep_target
    ep_target = None
    if piece.lower() == 'p' and abs(tr - sr) == 2:
        ep_target = ((sr + tr)//2, sc)
    # handle en-passant capture: if pawn moved to ep square but target was empty and ep_target prev existed
    if piece.lower()=='p' and captured == '.' and sc != tc and state['ep_target'] == (tr,tc):
        # capture pawn behind
        cap_r = tr + (1 if piece.isupper() else -1)
        captured = board[cap_r][tc]
        board[cap_r][tc] = '.'
    # promotion
    if piece.lower() == 'p' and (tr == 0 or tr == 7):
        promo_char = prom if prom else ('Q' if piece.isupper() else 'q')
        board[tr][tc] = promo_char
    # castling: move rook appropriately
    if piece.lower() == 'k' and castle != 0:
        # white king side
        if piece.isupper():
            if castle == 1:
                # rook from h1 (7,7) to f1 (7,5)
                board[7][5] = board[7][7]; board[7][7] = '.'
            else:
                # rook from a1 (7,0) to d1 (7,3)
                board[7][3] = board[7][0]; board[7][0] = '.'
        else:
            if castle == 1:
                board[0][5] = board[0][7]; board[0][7] = '.'
            else:
                board[0][3] = board[0][0]; board[0][0] = '.'
    # update castling rights
    cr = state['castling_rights'].copy()
    if piece == 'K': cr['K']=False; cr['Q']=False
    if piece == 'k': cr['k']=False; cr['q']=False
    if piece == 'R':
        if sr==7 and sc==0: cr['Q']=False
        if sr==7 and sc==7: cr['K']=False
    if piece == 'r':
        if sr==0 and sc==0: cr['q']=False
        if sr==0 and sc==7: cr['k']=False
    # if rook captured, update rights
    if captured == 'R':
        if tr==7 and tc==0: cr['Q']=False
        if tr==7 and tc==7: cr['K']=False
    if captured == 'r':
        if tr==0 and tc==0: cr['q']=False
        if tr==0 and tc==7: cr['k']=False

    new_state = {
        'board': board,
        'white_to_move': not state['white_to_move'],
        'castling_rights': cr,
        'ep_target': ep_target,
        'halfmove': 0 if piece.lower()=='p' or captured!='.' else state['halfmove']+1,
        'fullmove': state['fullmove'] + (1 if not state['white_to_move'] else 0)
    }
    return new_state

# -------- Attack detection and legality filtering ----------
def square_attacked(board, r, c, by_white):
    # check pawns
    if by_white:
        for dc in (-1,1):
            rr, cc = r+ -1, c + dc  # white pawns move up (decrease row)
            if inside(rr,cc) and board[rr][cc] == 'P':
                return True
    else:
        for dc in (-1,1):
            rr, cc = r+1, c + dc
            if inside(rr,cc) and board[rr][cc] == 'p':
                return True
    # knights
    for dr,dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
        rr, cc = r+dr, c+dc
        if inside(rr,cc):
            p = board[rr][cc]
            if p != '.' and ((by_white and p=='N') or (not by_white and p=='n')):
                return True
    # sliding: bishops/queens diagonals
    for dr,dc in [(-1,-1),(-1,1),(1,-1),(1,1)]:
        rr,cc = r+dr, c+dc
        while inside(rr,cc):
            p = board[rr][cc]
            if p != '.':
                if (by_white and (p=='B' or p=='Q')) or (not by_white and (p=='b' or p=='q')):
                    return True
                break
            rr+=dr; cc+=dc
    # sliding: rooks/queens orthogonal
    for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        rr,cc = r+dr, c+dc
        while inside(rr,cc):
            p = board[rr][cc]
            if p != '.':
                if (by_white and (p=='R' or p=='Q')) or (not by_white and (p=='r' or p=='q')):
                    return True
                break
            rr+=dr; cc+=dc
    # king adjacency
    for dr in (-1,0,1):
        for dc in (-1,0,1):
            if dr==0 and dc==0: continue
            rr,cc = r+dr, c+dc
            if inside(rr,cc):
                p = board[rr][cc]
                if (by_white and p=='K') or (not by_white and p=='k'):
                    return True
    return False

def legal_moves(state):
    pseudo = generate_pseudo_moves(state['board'], state['white_to_move'], state['castling_rights'], state['ep_target'])
    legal = []
    for mv in pseudo:
        new_state = make_move(state, mv)
        # find king position for side that just moved? Actually need to check king of the side to move (before switching)
        # After make_move we toggled white_to_move; so king to check is the opponent's king? Simpler: locate king of side that made the move and ensure not under attack
        # We want to ensure the player who moved did not leave his own king in check -> after move, opponent to move; so find king of side that moved (i.e., not new_state['white_to_move'])
        king_white = not new_state['white_to_move']
        kp = find_king(new_state['board'], king_white)
        if kp is None:
            continue
        kr,kc = kp
        if not square_attacked(new_state['board'], kr, kc, not king_white):
            # additional castling legality: ensure king not passing through attacked squares
            # if mv is castle, ensure the traversed squares are not attacked
            sr,sc,tr,tc,_,castle = mv
            if castle != 0:
                # squares between sr,sc and tr,tc (excluding original)
                step = 1 if tc > sc else -1
                ok=True
                # check starting square (should be not in check) and intermediate
                # starting square
                if square_attacked(state['board'], sr, sc, not state['white_to_move']):
                    ok=False
                # squares king passes through (one step and destination)
                c1 = sc + step
                c2 = sc + 2*step
                if square_attacked(state['board'], sr, c1, not state['white_to_move']):
                    ok=False
                if square_attacked(state['board'], tr, tc, not state['white_to_move']):
                    ok=False
                if not ok:
                    continue
            legal.append(mv)
    return legal

# -------- Game state initialization ----------
def new_game():
    return {
        'board': fen_to_board(START_FEN),
        'white_to_move': True,
        'castling_rights': {'K':True,'Q':True,'k':True,'q':True},
        'ep_target': None,
        'halfmove': 0,
        'fullmove': 1
    }

# -------- GUI drawing ----------
def draw_board(screen, state, selected, legal_moves_list, last_move):
    # board area: left square_size * 8
    for r in range(8):
        for c in range(8):
            x = c*TILE
            y = r*TILE
            color = LIGHT_SQUARE if (r+c)%2==0 else DARK_SQUARE
            pygame.draw.rect(screen, color, (x,y,TILE,TILE))
    # highlight last move
    if last_move:
        sr,sc,tr,tc,_,_ = last_move
        srect = pygame.Rect(sc*TILE, sr*TILE, TILE, TILE)
        trect = pygame.Rect(tc*TILE, tr*TILE, TILE, TILE)
        pygame.draw.rect(screen, (200,200,80,100), srect, 4)
        pygame.draw.rect(screen, (200,200,80,100), trect, 4)
    # highlight legal targets
    if selected:
        sr,sc = selected
        pygame.draw.rect(screen, (120,200,160,120), (sc*TILE, sr*TILE, TILE, TILE), 4)
        for mv in legal_moves_list:
            s = mv
            if s[0]==sr and s[1]==sc:
                tr,tc = s[2], s[3]
                center = (tc*TILE + TILE//2, tr*TILE + TILE//2)
                pygame.draw.circle(screen, BLUE, center, 8)
    # draw pieces
    for r in range(8):
        for c in range(8):
            p = state['board'][r][c]
            if p != '.':
                draw_piece(screen, p, c*TILE, r*TILE)
    # grid lines
    for i in range(9):
        pygame.draw.line(screen, BLACK, (0, i*TILE), (8*TILE, i*TILE))
        pygame.draw.line(screen, BLACK, (i*TILE, 0), (i*TILE, 8*TILE))

def draw_piece(screen, piece, x, y):
    # Simple text-based pieces
    color = WHITE if piece.isupper() else BLACK
    label = piece.upper()
    # large circle behind
    rect = pygame.Rect(x+8,y+8,TILE-16,TILE-16)
    pygame.draw.ellipse(screen, color, rect)
    # letter
    text = BIGFONT.render(label, True, (0,0,0) if piece.isupper() else (255,255,255))
    tw,th = text.get_size()
    screen.blit(text, (x + TILE//2 - tw//2, y + TILE//2 - th//2))

def draw_panel(screen, state, legal_len, in_check, game_over, winner, history):
    panel_x = 8*TILE
    pygame.draw.rect(screen, PANEL_BG, (panel_x,0,WIDTH-panel_x,HEIGHT))
    # turn
    turn = "White" if state['white_to_move'] else "Black"
    t_surf = BIGFONT.render(f"Turn: {turn}", True, TEXT_COLOR)
    screen.blit(t_surf, (panel_x + 12, 12))
    # castling rights
    cr = state['castling_rights']
    cr_text = f"Castling: K:{'Y' if cr['K'] else '-'} Q:{'Y' if cr['Q'] else '-'} k:{'Y' if cr['k'] else '-'} q:{'Y' if cr['q'] else '-'}"
    screen.blit(FONT.render(cr_text, True, TEXT_COLOR), (panel_x+12,44))
    # ep
    ep = state['ep_target']
    screen.blit(FONT.render(f"En-passant: {ep if ep else '-'}", True, TEXT_COLOR),(panel_x+12,64))
    # half/fullmove
    screen.blit(FONT.render(f"Fullmove: {state['fullmove']}  Halfmove: {state['halfmove']}", True, TEXT_COLOR), (panel_x+12,86))
    # legal move count
    screen.blit(FONT.render(f"Legal moves: {legal_len}", True, TEXT_COLOR),(panel_x+12,110))
    # check / game over
    if in_check:
        screen.blit(FONT.render("CHECK!", True, RED),(panel_x+12,136))
    if game_over:
        txt = "Checkmate!" if winner else "Stalemate!"
        screen.blit(BIGFONT.render(txt, True, RED), (panel_x+12, 160))
    # instructions
    lines = [
        "Click piece -> click dest to move",
        "U: Undo last move",
        "R: Restart",
        "Esc: Quit",
        "",
        "Move history:"
    ]
    y = 220
    for line in lines:
        screen.blit(FONT.render(line, True, TEXT_COLOR), (panel_x+12,y))
        y += 20
    # history (last 10)
    for i, h in enumerate(history[-10:]):
        screen.blit(FONT.render(h, True, TEXT_COLOR), (panel_x+12, y + i*18))

# -------- Game rules: check / mate detection ----------
def in_check(state, white):
    board = state['board']
    kp = find_king(board, white)
    if not kp: return True
    kr,kc = kp
    return square_attacked(board, kr, kc, not white)

def game_status(state):
    # returns (game_over_bool, winner_is_white_or_None_if_stalemate)
    legal = legal_moves(state)
    if len(legal) == 0:
        # if current side to move in check -> checkmate, winner is opponent
        if in_check(state, state['white_to_move']):
            return (True, not state['white_to_move'])
        else:
            return (True, None)  # stalemate
    return (False, None)

# -------- Simple algebraic-ish move notation for history ----------
def move_to_san(state, move):
    sr,sc,tr,tc,prom,castle = move
    cols = 'abcdefgh'
    s = f"{cols[sc]}{8-sr}->{cols[tc]}{8-tr}"
    if prom:
        s += f"={prom}"
    if castle==1:
        s += " (O-O)"
    if castle==2:
        s += " (O-O-O)"
    return s

# -------- Main loop ----------
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess - Local (PyGame)")
    clock = pygame.time.Clock()

    state = new_game()
    history_states = []
    history_moves = []
    selected = None
    legal = []
    dragging = False
    drag_piece = None
    last_move = None

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running=False
                if event.key == pygame.K_r:
                    state = new_game()
                    history_states = []
                    history_moves = []
                    selected = None
                    legal = []
                    last_move = None
                if event.key == pygame.K_u:
                    if history_states:
                        state = history_states.pop()
                        last_move = history_moves.pop() if history_moves else None
                        selected = None
                        legal = []
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx,my = event.pos
                if mx < 8*TILE and my < 8*TILE:
                    r = my // TILE; c = mx // TILE
                    p = state['board'][r][c]
                    if selected is None:
                        # select if piece of side to move
                        if p != '.' and ((state['white_to_move'] and p.isupper()) or (not state['white_to_move'] and p.islower())):
                            selected = (r,c)
                            legal = legal_moves(state)
                        else:
                            selected = None
                            legal = []
                    else:
                        # if clicked same square, deselect
                        if selected == (r,c):
                            selected = None; legal=[]
                        else:
                            # attempt move
                            found = None
                            for mv in legal:
                                if mv[0]==selected[0] and mv[1]==selected[1] and mv[2]==r and mv[3]==c:
                                    found = mv; break
                            if found:
                                history_states.append(deepcopy(state))
                                history_moves.append(found)
                                state = make_move(state, found)
                                last_move = found
                                selected = None
                                legal = []
                            else:
                                # if click your own piece, change selection
                                if p != '.' and ((state['white_to_move'] and p.isupper()) or (not state['white_to_move'] and p.islower())):
                                    selected = (r,c)
                                    legal = legal_moves(state)
                                else:
                                    selected = None; legal=[]
        # update UI status
        legal_now = legal_moves(state)
        inchk = in_check(state, state['white_to_move'])
        over, winner = game_status(state)

        # draw
        screen.fill((50,50,50))
        draw_board(screen, state, selected, legal_now, last_move)
        draw_panel(screen, state, len(legal_now), inchk, over, winner, [move_to_san(None, m) for m in history_moves])

        pygame.display.flip()

        if over:
            # game ended, still allow undo/restart; avoid auto-quit
            pass

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
