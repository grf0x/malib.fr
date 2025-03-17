<script>
    import Spinner from "../components/spinner.svelte";
    export let showProgressSpinner;
    export let theme;
    export let bookTitle = "-";
    export let chapterTitle = "-";
    export let bookProgress = 0;
    export let chapterProgress = 0;
    let heightBook = "2rem";
    let heightChapter = "2rem";
</script>

<div style="background-color:{theme.slider}; min-height:{heightChapter};" class="flex mb-2 self-center z-20 max-w-[90%] w-96 text-xs rounded-full">
{#if showProgressSpinner}
<div style="height:{heightChapter};" class="text-center w-full flex justify-center text-xs items-center">
    <Spinner color={theme.color} size="small"/>
</div> 
{:else}
    <div style="background-color:{theme.slider_range}; width:{chapterProgress > 10 ? chapterProgress : 10}%; height:{heightChapter};" class="flex rounded-full"></div>
    <div style="height:{heightChapter};" class="absolute pl-2 flex text-left text-[0.6rem] items-center opacity-70">
        {(chapterProgress).toFixed(2)}%
    </div>
    <div style="height:{heightChapter};" class="absolute max-w-[90%] w-96 px-12 text-center flex justify-center text-xs items-center">
        {chapterTitle}
    </div>
{/if}
</div>

<div style="min-height:{heightBook}; height:{heightBook}; background-color:{theme.slider};" class="flex w-full z-20">
{#if showProgressSpinner}
    <div style="height:{heightChapter};" class="text-center w-full flex justify-center text-xs items-center">
        <Spinner color={theme.color} size="small"/>
    </div> 
{:else}
    <div style="background-color:{theme.slider_range}; width:{bookProgress}%; height:{heightBook};" class="flex"></div>
    <div style="height:{heightBook};" class="absolute pl-2 flex text-left text-[0.6rem] items-center opacity-70">
        {#if bookProgress > 0}
        {(bookProgress).toFixed(2)}%
        {/if}
    </div>
    <div style="height:{heightBook};" class="absolute w-full pb-[0.2rem] text-center flex justify-center text-xs items-center">
        {bookTitle} 
    </div>
{/if}
</div>
