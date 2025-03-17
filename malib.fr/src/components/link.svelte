<script>
    import { goTo } from "../app.js";
    export let to;
    export let toExt;
    export let cls = "";

    function handleClick(){
        goTo(to);
    }
</script>
{#if toExt}
<a class={cls} href={toExt}><slot></slot></a>
{:else}
<a class={cls} href={to} on:click|preventDefault={handleClick}><slot></slot></a>
{/if}