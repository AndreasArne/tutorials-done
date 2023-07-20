<script lang="ts">
    import { user, userData } from "$lib/firebase";
    import "../app.css";

    // subscribe to stores globally
    $user;
    $userData;
</script>

<div class="min-h-screen flex flex-col">
<slot />
</div>