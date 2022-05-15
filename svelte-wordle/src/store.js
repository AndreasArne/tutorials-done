import {writable} from "svelte/store";

export function createGrid() {
    const grid = [];

    for (let i = 0; i<6; i++) {
        grid.push([]);
        for (let x = 0; x < 5; x++) grid[i][x] = "";
    }

    return grid;
}

export const board = writable(createGrid());
export const gameInfo = writable({
    char: 0,
    attempt: 0,
});
export const GAME_WORD = writable("HELLO");
export const guess = writable("");
export const colors = writable(createGrid());
export const gameOver = writable(false);
