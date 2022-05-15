<script>
    import { gameOver} from "./store";
    import Keyboard from "./components/Keyboard.svelte";
    import Board from "./components/Board.svelte";
    import GameOver from "./components/GameOver.svelte";
</script>

<main>
    <nav>Wordle Clone</nav>
    {#if $gameOver}
        <GameOver />
    {:else}
    <div>
        <Board />
        <Keyboard />
    </div>
    {/if}
</main>

<style>
    nav {
        background-color: var(--bg);
        color: white;
        font-weight: bold;
        padding: 15px;
        font-size: 2em;
        text-align: center;
    }
</style>