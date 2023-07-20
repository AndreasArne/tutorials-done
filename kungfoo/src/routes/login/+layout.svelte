<script lang="ts">
    import {page} from "$app/stores";
    import AnimatedRoute from "$lib/components/AnimatedRoute.svelte";
</script>


<nav class="flex justify-center my-6">
    <ul class="steps">
        <a href="/login" class="step step-primary">Sign in</a>
        <!--
            https://svelte.dev/tutorial/classes
            https://learn.svelte.dev/tutorial/page-store
         -->
        <a href="/login/username"
            class="step"
            class:step-primary={$page.route.id?.match(/username|photo/g)}> 
            Choose username
        </a>
        <a 
            href="/login/photo" 
            class="step"
            class:step-primary={$page.route.id?.match(/photo/g)}>
            Upload Photo
        </a>
    </ul>
</nav>

<AnimatedRoute>
<main class="card w-4/6 bg-neutral text-neutral-content mx-auto">
    <div class="card-body items-center text-center">
        <slot></slot>

    </div>
</main>
</AnimatedRoute>