<script context="module">
    export async function load({ fetch }) {
        // const res = await fetch("https://jsonplaceholder.typicode.com/posts")
        const res = await fetch("/guides.json")
        const { guides } = await res.json()

        if (res.ok) {
            return {
                props: {
                    guides // om nyckel har samma namn som variabel högre upp, används variabeln automatiskt som värde
                }
            }
        }
        return {
            status: res.status,
            error: new Error("Could not fetch the guides")
        }
    }
</script>

<script>
    export let guides
</script>

<div class="guides">
    <ul>
        {#each guides as guide}
            <li>
                <a sveltekit:prefetch href={`/guides/${guide.id}`}>{guide.title}</a> <!-- sveltekit:prefetch gör att svelte automatisk prefetchar datan när man hovrar på länken -->
            </li>
        {/each}
    </ul>
</div>

<style>
    .guides {
        margin-top: 20px;
    }
    ul {
        list-style-type: none;
        padding: 0;
    }
    a {
        display: inline-block;
        margin-top: 10px;
        padding: 10px;
        border: 1px dotted rgba(255,255,255,0.2);
    }
</style>