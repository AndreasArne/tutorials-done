<script lang="ts">
    import {onMount } from "svelte"
    import { blur } from "svelte/transition"
    import {tweened} from "svelte/motion"

    type Game = "waiting for input" | "in progress" | "game over"
    type Word = string

    let game: Game = "waiting for input"
    let seconds = 30
    let typedLetter = ""

    let words: Word[] = []

    let wordIndex = 0
    let letterIndex = 0
    let correctLetters = 0
    let toggleReset = false

    let wordsPerMinute = tweened(0, { delay: 300, duration: 1000})
    let accuracy = tweened(0, { delay: 1300, duration: 1000})

    let wordsEl: HTMLDivElement
    let letterEl: HTMLSpanElement
    let inputEl: HTMLInputElement
    let caretEl: HTMLDivElement

    function resetGame() {
        toggleReset = !toggleReset

        setGameState("waiting for input")
        getWords(100)
        
        seconds = 30
        typedLetter = ""
        wordIndex = 0
        letterIndex = 0
        correctLetters = 0

        $wordsPerMinute = 0
        $accuracy = 0
    }

    function getWordsPerMinute() {
        const word = 5
        const minutes = 0.5

        return Math.floor(correctLetters / word / minutes)
    }

    function getResults() {
        $wordsPerMinute = getWordsPerMinute()
        $accuracy = getAccuracy()
    }

    function getAccuracy() {
        const totalLetters = getTotalLetters(words)
        return Math.floor(correctLetters / totalLetters * 100)
    }

    function getTotalLetters(words: Word[]) {
        return words.reduce((count, word) => count + word.length, 0)
    }


    function updateGameState() {
        setLetter()
        checkLetter()
        nextLetter()
        updateLine()
        resetLetter()
        moveCaret()
    }

    function setLetter() {
        const isWordCompleted = letterIndex > words[wordIndex].length - 1

        if (!isWordCompleted) {
            letterEl = wordsEl.children[wordIndex].children[letterIndex] as HTMLSpanElement

        }
    }

    function checkLetter() {
        const currentLetter = words[wordIndex][letterIndex]

        if (typedLetter === currentLetter) {
            letterEl.dataset.letter = "correct"
            increaseScore()
        }
        
        if (typedLetter !== currentLetter) {
            letterEl.dataset.letter = "incorrect"
        }
    }

    function increaseScore() {
        correctLetters += 1
    }

    function nextLetter() {
        letterIndex += 1
    }

    function nextWord() {
        const isNotFirstLetter = letterIndex !== 0
        const isOneLetterWord = words[wordIndex].length === 1

        if (isNotFirstLetter || isOneLetterWord) {
            wordIndex += 1
            letterIndex = 0
            increaseScore()
            moveCaret()
        }
    }

    function updateLine() {
        const wordEl = wordsEl.children[wordIndex]
        const wordsY = wordsEl.getBoundingClientRect().y
        const wordY = wordEl.getBoundingClientRect().y

        console.log({ wordsY, wordY});
        
        if (wordY > wordsY) {
            wordEl.scrollIntoView({ block:"center"})
        }
    }

    function resetLetter() {
        typedLetter = ""
    }

    function moveCaret() {
        const offset = 4
        const { offsetLeft, offsetTop, offsetWidth } = letterEl

        caretEl.style.top = `${offsetTop + offset}px`
        caretEl.style.left = `${offsetLeft + offsetWidth}px`
    }

    function startGame() {
        setGameState("in progress")
        setGameTimer()
    }

    function setGameState(state: Game) {
        game = state
    }

    function setGameTimer() {
        function gameTimer() {
            if (seconds > 0) {
                seconds -= 1
            }

            if (game === "waiting for input" || seconds === 0) {
                clearInterval(interval)
            }

            if (seconds === 0) {
                setGameState("game over")
                getResults()
            }
        }
        const interval = setInterval(gameTimer, 1000)
    }

    async function getWords(limit: number) {
        const respons = await fetch(`/api/words?limit=${limit}`)
        words = await respons.json()
    }

    function focusInput() {
        inputEl.focus()
    }

    function handleKeydown(event: KeyboardEvent) {
        if (event.code === "Space") {
            event.preventDefault()

            if (game === "in progress") {
                nextWord()
            }
        }

        if (game === "waiting for input") {
            startGame()
        }
    }

    onMount(() => {
        getWords(100)
        focusInput()
    })
</script>

{#if game !== "game over"}
<div class="game" data-game={game}>
    <input 
        bind:this={inputEl}
        bind:value={typedLetter}
        on:input={updateGameState}
        on:keydown={handleKeydown}
        type="text"
        class="input"
    />

    <div class="time">{seconds}</div>

    {#key toggleReset}
        <div in:blur|local class="words" bind:this={wordsEl}>
            {#each words as word}
            <span class="word">
                {#each word as letter}
                    <span class="letter">{letter}</span>
                {/each}
            </span>
            {/each}
            <div class="caret" bind:this={caretEl}></div>
        </div>
    {/key}
    <div class="reset">
        <button on:click={resetGame} aria-label="reset">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          width="24"
          height="24"
          stroke-width="1.5"
          stroke="currentColor"
          fill="none"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M15 15l6-6m0 0l-6-6m6 6H9a6 6 0 000 12h3"
          />
        </svg>
      </button>
    </div>
</div>
{/if}

{#if game === "game over"}
    <div in:blur class="results">
        <div>
            <p class="title">wpm</p>
            <p class="score">{Math.trunc($wordsPerMinute)}</p>
        </div>
        <div>
            <p class="title">accuracy</p>
            <p class="score">{Math.trunc($accuracy)}%</p>
        </div>
        <div on:click={resetGame} class="play">Play again</div>
    </div>
{/if}

<style lang="scss">

    .game {
        position: relative;

        .input {
            position: absolute;
            opacity: 0;
        }
        
        .time {
            position: absolute;
            top: -48px;
            font-size: 1.5rem;
            color: var(--primary);
            opacity: 0;
            transition: all 0.3s ease;
        }

        &[data-game="in progress"] .time {
            opacity: 1;
        }

        .reset {
            width: 100%;
            display: grid;
            justify-content: center;
            margin-top: 2rem;
        }
    }


  .words {
    --line-height: 1em;
    --lines: 3;

    width: 100%;
    max-height: calc(var(--line-height) * var(--lines) * 1.42);
    display: flex;
    flex-wrap: wrap;
    gap: 0.6em;
    position: relative;
    font-size: 1.5rem;
    line-height: var(--line-height);
    overflow: hidden;
    user-select: none;

    .letter {
      opacity: 0.4;
      transition: all 0.3s ease;

    // should work but doesn't. Might be the svelte version. Seems they have had problems with it
    //   &:global([data-letter='correct']) {
    //     opacity: 0.8;
    //   }

    //   &:global([data-letter='incorrect']) {
    //     color: var(--primary);
    //     opacity: 1;
    //   }
    }

    :global([data-letter='correct']) {
        opacity: 0.8 !important;
    }

    :global([data-letter='incorrect']) {
        color: var(--primary);
        opacity: 1 !important;
      }

      .caret {
        position: absolute;
        height: 1.8rem;
        top: 0;
        border-right: 1px solid var(--primary);
        animation: caret 1s infinite;
        transition: all 0.2s ease;

        @keyframes caret {
            0% {
                opacity: 0;
            }
            50% {
                opacity: 1;
            }
        }
      }
  }

  .results {
    .title {
        font-size: 2rem;
        color: var(--fg-200);
    }

    .score {
        font-size: 4rem;
        color: var(--primary);
    }
    .play {
        margin-top: 1rem;
    }
  }
</style>