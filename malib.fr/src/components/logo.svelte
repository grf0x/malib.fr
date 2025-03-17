<script>
    import { createEventDispatcher } from 'svelte';
    import * as conf from "../app.json";
    import Link from "./link.svelte";
    export let color = "#fff";
    const dispatch = createEventDispatcher();
    function onClick(){dispatch("click");}
</script>

<div on:click={onClick} style="color:{color}" class="pt-2 pb-1 font-malib cursor-pointer text-4xl">
    Malib
</div>
