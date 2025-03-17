<script>
    import { createEventDispatcher, onDestroy, onMount } from "svelte";

    export let hideAndShow = false;
    let show = !hideAndShow;
    let observer;
    let target;
    const dispatch= createEventDispatcher();

    function handleInstersection(entries){
        if(entries[0].isIntersecting)
        {
            show = true;
            dispatch("inview");
        }
    };

    onMount(() => {
        observer = new IntersectionObserver(handleInstersection);
        observer.observe(target);
    });

    onDestroy(() => {
        if(observer !== undefined)
            observer.disconnect();
    });
</script>
  
<div bind:this={target}>
    {#if show}
    <slot></slot>
    {/if}
</div>
  