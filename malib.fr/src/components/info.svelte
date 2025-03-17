<script>
    import { createEventDispatcher } from 'svelte';
    import * as conf from "../app.json";
    export let title = "";
    export let content = "";
    export let showContent = false;
    let visible = true;

    const dispatch = createEventDispatcher();
    function onClick(){
        visible = false;
        dispatch("close");
    }
</script>

{#if visible}
<div on:click={()=>{showContent=!showContent}} class="flex flex-col fixed bottom-2 right-2 rounded-lg z-[60] bg-neutral-700 text-white shadow-md shadow-black text-sm w-72 md:w-[22rem] py-6 px-8 cursor-pointer">
    <span on:click={onClick} class="fixed flex -ml-7 -mt-5 text-neutral-300 bg-neutral-600 w-5 h-5 items-center justify-center rounded-full  text-xs">x</span>
    <span class="font-bold">{title}</span>
    {#if showContent}
    <span class="mt-2">{content}</span>
    {:else}
    <span >{conf.info.click_me}</span>
    {/if}
</div>
{/if}

