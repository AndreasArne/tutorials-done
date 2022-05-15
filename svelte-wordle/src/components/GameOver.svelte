<script>
    import { gameInfo, gameOver, GAME_WORD, guess, colors, createGrid, board} from "../store";
    import Board from "./Board.svelte";

    const playAgain = () => {
        const wordsList = ["COLOR", "GREET", "GRUMP", "YIELD"];
        const word = wordsList[Math.floor(Math.random()*wordsList.length)];
        GAME_WORD.set(word);
        gameInfo.set({
            attempt: 0,
            char: 0
        });
        guess.set("");
        colors.set(createGrid());
        board.set(createGrid());
        gameOver.set(false);
    }
</script>
<div class="center">
    <h3>The correct word was: <strong>{$GAME_WORD}</strong></h3>
    <h3>You guessed: <strong>{$guess}</strong></h3>
</div>

<Board />

<div class="center">
    <button on:click={playAgain}>Play Again?</button>
</div>
<style>
    strong {
        font-weight: 900;
    }
    h3 {
        font-size: 2em;
    }
    button {
        background-color: var(--orange);
        color: white;
        margin-top: 20px 50px;
        padding: 20px 50px;
        cursor: pointer;
        border: none;
    }
    .center {
        margin: 20px auto;
        width: fit-content;
        text-align: center;
    }
</style>