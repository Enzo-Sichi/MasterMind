import streamlit as st
from typing import List, Tuple
import random

# Set page config
st.set_page_config(
    page_title="Mastermind Color Game",
    page_icon="🎨",
    layout="centered"
)

# Define colors
COLORS = {
    "Red": "#FF0000",
    "Blue": "#0000FF",
    "Green": "#00FF00",
    "Yellow": "#FFD700",
    "Purple": "#800080",
    "Orange": "#FFA500"
}

# Initialize session state variables
if 'secret_code' not in st.session_state:
    st.session_state.secret_code = []
if 'attempts' not in st.session_state:
    st.session_state.attempts = []
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'max_attempts' not in st.session_state:
    st.session_state.max_attempts = 10
if 'game_mode' not in st.session_state:
    st.session_state.game_mode = None
if 'code_set' not in st.session_state:
    st.session_state.code_set = False

def generate_secret_code(length: int = 4) -> List[str]:
    """Generate a random secret code of specified length with colors"""
    return random.choices(list(COLORS.keys()), k=length)

def check_guess(secret_code: List[str], guess: List[str]) -> Tuple[int, int]:
    """
    Check the guess against the secret code
    Returns (correct_position, correct_color)
    """
    correct_position = 0
    correct_color = 0
    
    # Count correct positions
    for s, g in zip(secret_code, guess):
        if s == g:
            correct_position += 1
    
    # Count correct colors in wrong positions
    secret_counts = {color: 0 for color in COLORS}
    guess_counts = {color: 0 for color in COLORS}
    
    for s, g in zip(secret_code, guess):
        if s != g:
            secret_counts[s] += 1
            guess_counts[g] += 1
    
    for color in COLORS:
        correct_color += min(secret_counts[color], guess_counts[color])
    
    return correct_position, correct_color

def new_game():
    """Initialize a new game"""
    st.session_state.secret_code = []
    st.session_state.attempts = []
    st.session_state.game_over = False
    st.session_state.code_set = False
    st.session_state.game_mode = None

def display_color_circle(color: str):
    """Display a colored circle with the color name"""
    return f'<div style="display: inline-block; margin: 0 5px; width: 25px; height: 25px; border-radius: 50%; background-color: {COLORS[color]}; border: 1px solid black;" title="{color}"></div>'

def main():
    st.title("🎨 Mastermind Color Game")
    
    # Rules in expander
    with st.expander("📖 How to Play"):
        st.markdown("""
        ### Rules of Mastermind
        
        1. Choose game mode:
           - **Single Player**: Computer generates a secret code
           - **Multiplayer**: Player 1 sets the code, Player 2 guesses
        2. The code consists of 4 colors (can repeat)
        3. Player has 10 attempts to guess the correct code
        4. After each guess, you'll receive feedback:
           - 🎯 Number of correct colors in correct positions
           - ⭕ Number of correct colors in wrong positions
        
        **Available Colors**: Red, Blue, Green, Yellow, Purple, Orange
        
        Good luck! 🍀
        """)
    
    # New game button
    if st.button("New Game"):
        new_game()
    
    # Game mode selection if not already selected
    if not st.session_state.game_mode:
        st.write("### Select Game Mode")
        col1, col2 = st.columns(2)
        if col1.button("Single Player"):
            st.session_state.game_mode = "single"
            st.session_state.secret_code = generate_secret_code()
            st.session_state.code_set = True
            st.rerun()
        if col2.button("Multiplayer"):
            st.session_state.game_mode = "multi"
            st.rerun()
    
    # Multiplayer code setting
    if st.session_state.game_mode == "multi" and not st.session_state.code_set:
        st.write("### Player 1: Set Secret Code")
        st.write("Choose 4 colors:")
        
        secret_code = []
        cols = st.columns(4)
        for i in range(4):
            color = cols[i].selectbox(
                f"Color {i+1}",
                options=list(COLORS.keys()),
                key=f"secret_{i}"
            )
            secret_code.append(color)
        
        if st.button("Set Code"):
            st.session_state.secret_code = secret_code
            st.session_state.code_set = True
            st.rerun()
            
    # Main game interface
    if st.session_state.code_set and not st.session_state.game_over:
        st.write("### Make Your Guess!")
        remaining_attempts = st.session_state.max_attempts - len(st.session_state.attempts)
        st.write(f"Remaining attempts: {remaining_attempts}")
        
        # Color selection for guess
        guess = []
        cols = st.columns(4)
        for i in range(4):
            color = cols[i].selectbox(
                f"Color {i+1}",
                options=list(COLORS.keys()),
                key=f"guess_{i}"
            )
            guess.append(color)
        
        # Display current guess as colored circles
        st.write("Current guess:")
        guess_html = "".join([display_color_circle(color) for color in guess])
        st.markdown(guess_html, unsafe_allow_html=True)
        
        # Submit guess button
        if st.button("Submit Guess"):
            correct_pos, correct_color = check_guess(st.session_state.secret_code, guess)
            st.session_state.attempts.append({
                'guess': guess,
                'correct_position': correct_pos,
                'correct_color': correct_color
            })
            
            # Check win condition
            if correct_pos == 4:
                st.session_state.game_over = True
                st.balloons()
                st.success("🎉 Congratulations! You've cracked the code!")
            elif remaining_attempts <= 1:
                st.session_state.game_over = True
                st.error("Game Over!")
                st.write("The secret code was:")
                solution_html = "".join([display_color_circle(color) for color in st.session_state.secret_code])
                st.markdown(solution_html, unsafe_allow_html=True)
    
    # Display previous attempts
    if st.session_state.attempts:
        st.write("### Previous Attempts")
        for i, attempt in enumerate(st.session_state.attempts):
            st.write(f"Attempt {i+1}:")
            guess_html = "".join([display_color_circle(color) for color in attempt['guess']])
            st.markdown(guess_html + f" | 🎯 Correct positions: {attempt['correct_position']} | ⭕ Correct colors: {attempt['correct_color']}", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
