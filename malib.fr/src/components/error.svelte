<script>
    import { fade } from 'svelte/transition';
    let show = false;
    let message = "";
    let fadeDuration = 1000;
    export let cls = "";

    export const funcs = {
        show(msg){message = msg; show = true;},
        hide(){show = false; message = "";}
    }
</script>

{#if show}
<div in:fade={{duration:fadeDuration}} class={cls}>
    {message}
</div>
{/if}