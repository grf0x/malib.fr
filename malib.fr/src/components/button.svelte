<script>
    import { createEventDispatcher } from 'svelte';
    import Spinner from "../components/spinner.svelte";
    import Link from "../components/link.svelte";
    export let to;
    export let toExt;
    export let size = "base";
    export let cls = ""
    export let showSpinner = false;
    export let theme = "normal";
    let sharedCls = "flex items-center justify-center select-none";
    let styleCls;
    let sizeCls;

    const dispatch = createEventDispatcher();
    function onClick(){
        if(!showSpinner)
            dispatch("click");
    }

    if(theme == "black")
        styleCls = "text-white bg-black hover:brightness-150 transition ease-in-out duration-300";
    else if(theme == "darkGrey")
        styleCls = "text-white bg-neutral-800 hover:brightness-150 transition ease-in-out duration-300";
    else if(theme == "whiteBox")
        styleCls = "text-white border border-white hover:border-neutral-300 hover:text-neutral-200 transition ease-in-out duration-300";
    else
        styleCls = "text-white bg-gradient-to-r from-custom-red-dark to-custom-red-light hover:brightness-110 transition ease-in-out duration-300";

    if(size == "tiny")
        sizeCls = "py-1 px-1 text-[0.55rem] rounded";
    else if(size == "small")
        sizeCls = "py-[0.65rem] px-2 text-sm rounded-lg";
    else if(size == "medium")
        sizeCls = "px-6 py-3 mdtext-lg text-base rounded-lg font-semibold";
    else if(size == "big")
        sizeCls = "px-8 py-4 md:text-xl text-lg rounded-lg font-semibold";
    else if(size == "vbig")
        sizeCls = "px-12 py-4 text-2xl rounded-lg font-semibold";
    else
        sizeCls = "px-6 py-3 mdtext-lg text-base rounded-lg font-semibold";


    $: classes = sharedCls + " " + sizeCls + " " + styleCls;
</script>

{#if to}
<Link {to} on:click={onClick} cls={classes + " " + cls}>
    {#if showSpinner}
    <span class="opacity-0"><slot></slot></span><div class="absolute"><Spinner size={size + "_button"} color="white"/></div>
    {:else}
    <slot></slot>
    {/if}
</Link>
{:else if toExt}
<Link {toExt} on:click={onClick} cls={classes + " " + cls}>
    {#if showSpinner}
    <span class="opacity-0"><slot></slot></span><div class="absolute"><Spinner size={size + "_button"} color="white"/></div>
    {:else}
    <slot></slot>
    {/if}
</Link>
{:else}
<button on:click={onClick} class={classes + " " + cls} disabled={showSpinner}>
    {#if showSpinner}
    <span class="opacity-0"><slot></slot></span><div class="absolute"><Spinner size={size + "_button"} color="white"/></div>
    {:else}
    <slot></slot>
    {/if}
</button>
{/if}