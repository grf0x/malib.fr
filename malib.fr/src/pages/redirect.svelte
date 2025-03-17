<script>
    export let page;
    import { onMount } from "svelte";
    import { goTo } from "../app.js";

    onMount(async()=>{
        goTo(page);
    });
</script>