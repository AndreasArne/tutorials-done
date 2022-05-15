<script>
    import Key from "./Key.svelte";
    import { board, gameInfo, colors, GAME_WORD, guess, gameOver } from "../store";

    const row1 = ["q","w","e","r","t","y","u","i","o","p"];
    const row2 = ["a","s","d","f","g","h","j","k","l"];
    const row3 = ["ENTER","z","x","c","v","b","n","m", "DEL"];

    const handleDel = () => {
        if ($gameInfo.char === 0)
            return;
        
        gameInfo.update((prev) => {
            return {
                char: prev.char - 1,
                attempt: prev.attempt
            };
        })
        board.update((prev) => {
            const newBoard = prev;
            newBoard[$gameInfo.attempt][$gameInfo.char] = "";
            return newBoard;
        })
    }
    const handleEnter = () => {
        let {attempt, char} = $gameInfo;

        if (char !== 5)
            return;
        
        gameInfo.set({
            attempt: attempt+1,
            char: 0,
        })

        const prevAttempt = $gameInfo.attempt - 1;
        const newColorsBoard = $colors;
        const duplicateChars = new Set();

        for (let i = 0; i < 5; i++) {
            let char = $board[prevAttempt][i].toUpperCase();
            guess.update((prevChars) => prevChars + char);

            if ($GAME_WORD[i].toUpperCase() === char)
                newColorsBoard[prevAttempt][i] = "correct";
            else if ($GAME_WORD.toUpperCase().includes(char)) {
                if (!duplicateChars.has(char)) {
                    newColorsBoard[prevAttempt][i] = "close";
                    duplicateChars.add(char);
                }
            } else {
                newColorsBoard[prevAttempt][i] = "incorrect";
            }
        }
        colors.set(newColorsBoard);

        if ($guess.toUpperCase() === $GAME_WORD.toUpperCase() || prevAttempt === 5)
            gameOver.set(true);
        else
            guess.set("");
    }

    const keyPress = (key = "") => {
        if (key === "DEL")
            handleDel();
        else if (key === "ENTER")
            handleEnter();
        else {
            let { attempt, char } = $gameInfo;
            if (char > 4)
                return;
            board.update((previous) => {
                const newBoard = previous;
                newBoard[attempt][char++] = key;
                return newBoard;
            })
            gameInfo.set({attempt, char});
        }
    }
</script>

<div class="keyboard">
    <div class="row">
        {#each row1 as char}
            <Key {char} {keyPress}/>
        {/each}
    </div>
    <div class="row">
        {#each row2 as char}
            <Key {char} {keyPress}/>
        {/each}
    </div>
    <div class="row">
        {#each row3 as char}
            <Key {char} {keyPress}/>
        {/each}
    </div>
</div>

<style>
    .keyboard{
        position: fixed;
        width: fit-content;
        bottom: 20px;
        left: 50%;
        transform: translate(-50%, 0%);
    }

    .row {
        display: flex;
        align-items: center;
        justify-content: center;
    }
</style>