<script>
    import { fade, slide, scale } from "svelte/transition";
    import { flip } from "svelte/animate";
    import PollDetails from "./pollDetails.svelte";
    import PollStore from "../stores/pollStore.js";

</script>



<!-- local sätter att animationen bara ska ske om ett individuellt elemnt försvinner och inte alla. Så på "delete" -->
<!-- Kan bara göra transistions på html elemnt och inte komponenter.-->
<div class="poll-list">
    {#each $PollStore as poll (poll.id)}
        <div in:fade out:scale|local animate:flip={{duration: 500}}>
            <PollDetails {poll} />
        </div>
    {/each}
</div>



<style>
    .poll-list {
        display: grid;
        grid-template-columns: 1fr 1fr;
        grid-gap: 20px;
    }
</style>
