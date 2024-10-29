import streamlit as st
import random
from typing import List, Tuple
import json

# Set page config
st.set_page_config(
    page_title="Mastermind Game",
    page_icon="🎯",
    layout="centered"
)

# Initialize session state variables
if 'secret_code' not in st.session_state:
    st.session_state.secret_code = []
if 'attempts' not in st.session_state:
    st.session_state.attempts = []
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'max_attempts' not in st.session_state:
    st.session_state.max_attempts = 10

def generate_secret_code(length: int = 4) -> List[int]:
    """Generate a random secret code of specified length with numbers 1-6"""
    return [random.randint(1, 6) for _ in range(length)]

def check_guess(secret_code: List[int], guess: List[int]) -> Tuple[int, int]:
    """
    Check the guess against the secret code
    Returns (correct_position, correct_number)
    """
    correct_position = 0
    correct_number = 0
    
    # Count correct positions
    for s, g in zip(secret_code, guess):
        if s == g:
            correct_position += 1
    
    # Count correct numbers
    secret_counts = [0] * 7
    guess_counts = [0] * 7
    
    for s, g in zip(secret_code, guess):
        if s != g:
            secret_counts[s] += 1
            guess_counts[g] += 1
    
    for i in range(1, 7):
        correct_number += min(secret_counts[i], guess_counts[i])
    
    return correct_position, correct_number

def new_game():
    """Initialize a new game"""
    st.session_state.secret_code = generate_secret_code()
    st.session_state.attempts = []
    st.session_state.game_over = False

def main():
    st.title("🎯 Mastermind Game")
    
    # Rules in expander
    with st.expander("📖 How to Play"):
        st.markdown("""
        ### Rules of Mastermind
        
        1. The computer generates a secret code of 4 numbers (1-6).
        2. You have 10 attempts to guess the correct code.
        3. After each guess, you'll receive feedback:
           - 🎯 Number of correct digits in correct positions
           - ⭕ Number of correct digits in wrong positions
        4. Use this feedback to deduce the secret code!
        
        **Example:**
        - Secret code: [1, 2, 3, 4]
        - Your guess: [1, 3, 2, 6]
        - Feedback: 1 correct position (1), 2 correct numbers in wrong positions (2,3)
        
        Good luck! 🍀
        """)
    
    # New game button
    if st.button("New Game"):
        new_game()
    
    # Initialize game if not started
    if not st.session_state.secret_code:
        new_game()
    
    # Display remaining attempts
    remaining_attempts = st.session_state.max_attempts - len(st.session_state.attempts)
    st.write(f"Remaining attempts: {remaining_attempts}")
    
    # Game input
    if not st.session_state.game_over and remaining_attempts > 0:
        cols = st.columns(4)
        guess = []
        for i in range(4):
            guess.append(cols[i].number_input(
                f"Position {i+1}",
                min_value=1,
                max_value=6,
                value=1,
                key=f"guess_{i}"
            ))
        
        # Submit guess button
        if st.button("Submit Guess"):
            correct_pos, correct_num = check_guess(st.session_state.secret_code, guess)
            st.session_state.attempts.append({
                'guess': guess,
                'correct_position': correct_pos,
                'correct_number': correct_num
            })
            
            # Check win condition
            if correct_pos == 4:
                st.session_state.game_over = True
                st.balloons()
                st.success("🎉 Congratulations! You've cracked the code!")
            elif remaining_attempts <= 1:
                st.session_state.game_over = True
                st.error(f"Game Over! The secret code was {st.session_state.secret_code}")
    
    # Display previous attempts
    if st.session_state.attempts:
        st.write("### Previous Attempts")
        for i, attempt in enumerate(st.session_state.attempts):
            st.write(f"Attempt {i+1}: {attempt['guess']} | "
                    f"🎯 Correct positions: {attempt['correct_position']} | "
                    f"⭕ Correct numbers: {attempt['correct_number']}")

if __name__ == "__main__":
    main()
