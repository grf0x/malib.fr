<script>
    export let tocList;
    export let theme;
    export let reader;
    export let currentHref;
</script>

<div style="color:{theme.background};max-height: calc(100vh - 10rem);" class="flex flex-col select-none overflow-scroll no-scrollbar">
    {#each tocList as chapter}
    <div on:click={()=>{reader.display(chapter.href)}} class="flex w-full items-center py-4 px-8 cursor-pointer font-futurar"> 
        {#if currentHref == chapter.href}
        <svg fill={theme.background} class="-ml-5 mr-2 w-3 h-3 shrink-0" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 405.272 405.272" style="enable-background:new 0 0 405.272 405.272;"	 xml:space="preserve"><g>	<path d="M393.401,124.425L179.603,338.208c-15.832,15.835-41.514,15.835-57.361,0L11.878,227.836		c-15.838-15.835-15.838-41.52,0-57.358c15.841-15.841,41.521-15.841,57.355-0.006l81.698,81.699L336.037,67.064		c15.841-15.841,41.523-15.829,57.358,0C409.23,82.902,409.23,108.578,393.401,124.425z"/></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g></svg>
        {/if}
        {#if chapter.level === 0}
        <span class="contrast-200 font-bold">{chapter.label}</span>
        {:else if chapter.level === 1}
        <span class="opacity-80">{chapter.label}</span>
        {:else}
        <span class="opacity-80">
            {#each Array(chapter.level - 1) as _}
            <span class="mr-4">•</span>
            {/each}
            {chapter.label}
        </span>
        {/if}
        
    </div>
    <hr style="border-top:1px solid {theme.background}">
    {/each}
</div>
