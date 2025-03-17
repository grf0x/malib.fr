<script>
    import { slide } from 'svelte/transition';
    export let question = "";
    export let answer = "";
    export let duration = 400;
    let open = false;
</script>

<div on:click={() => open = !open} class="md:p-8 p-6 space-y-4 bg-neutral-800 rounded-lg cursor-pointer select-none">
    <h2 class="md:text-xl text-lg">{question}</h2>
    {#if open}
    <p transition:slide={{duration}} class="md:text-xl text-lg">{answer}</p>
    {/if}
</div>