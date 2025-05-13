import streamlit as st
import numpy as np

ROWS, COLS = 6, 7
EMPTY = ""

if "board" not in st.session_state:
  st.session_state.board = np.full((ROWS, COLS), EMPTY)
  st.session_state.turn = "R"
  st.session_state.winner = None

def drop_piece(col):
  for row in reversed(range(ROWS)):
    if st.session_state.board[row][col] == EMPTY:
      st.session_state.board[row][col] = st.session_state.turn
      if check_winner(row, col):
        st.session_state.winner = st.session_state.turn
      else:
        st.session_state.turn = "Y" if st.session_state.turn == "R" else "R"
      break

def check_winner(row, col):
  def count_dir(dr, dc):
    r, c = row + dr, col + dc
    count = 0
    while 0 <= r < ROWS and 0 <= c < COLS and st.session_state.board[r][c] == st.session_state.turn:
      count += 1
      r += dr
      c += dc
    return count

  directions = [(0,1), (1,0), (1,1), (1,-1)]
  for dr, dc in directions:
    total = 1 + count_dir(dr, dc) + count_dir(-dr, -dc)
    if total >= 4:
      return True
  return False

def reset_game():
  st.session_state.board = np.full((ROWS, COLS), EMPTY)
  st.session_state.turn = "R"
  st.session_state.winner = None

st.title("Connect 4")

drop_cols = st.columns(COLS)
for i in range(COLS):
  disabled = st.session_state.winner is not None
  if drop_cols[i].button("*", key=f"drop_{i}", disabled=disabled):
    if EMPTY in st.session_state.board[:, i]:
      drop_piece(i)

if st.session_state.winner:
  st.write(f"Winner: {'R' if st.session_state.winner == 'R' else 'Y'}")
else:
  st.write(f"Turn: {'R' if st.session_state.turn == 'R' else 'Y'}")

for row in range(ROWS):
  cols = st.columns(COLS)
  for col in range(COLS):
    piece = st.session_state.board[row][col]
    color = "- "
    if piece == "R":
      color = "R"
    elif piece == "Y":
      color = "Y"
    cols[col].markdown(f"<h1 style='text-align: center'>{color}</h1>", unsafe_allow_html=True)

if st.session_state.winner:
  st.success(f"{'R' if st.session_state.winner == 'R' else 'Y'} wins!")

if st.button("Reset Game"):
  reset_game()
