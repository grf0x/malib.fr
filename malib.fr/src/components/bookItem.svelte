<script>
    import * as conf from "../app.json";
    import { goTo } from "../app.js";
    import { createEventDispatcher } from "svelte";
    export let title;
    export let author;
    export let clickable = false;
    export let librarySize = false;
    export let placeholder = false;
    export let cls = "";
    export let progress = 0;
    let librarySizeTitleCls = " text-[4vw] md:text-[2.1vw] lg:text-[1.4vw] 2xl:text-[1vw]";
    let librarySizeAuthorCls = " text-[3.4vw] md:text-[1.8vw] lg:text-[1.2vw] 2xl:text-[0.9vw]";
    let clickableCls = " hover:brightness-110 transition ease-in-out duration-300 cursor-pointer";

    const dispatch = createEventDispatcher();
    function onClick(){dispatch("click");}
</script>

{#if placeholder}
<div class={"flex justify-center w-full " + cls}>
    <div class="relative h-0 pb-[130%] w-full text-neutral-900">
        <div on:click={onClick}  class={"absolute select-none w-full h-full rounded-sm" }>
            <div class="flex w-full h-full border-neutral-800 border flex-col text-center place-content-between p-[4%]">            
                <div class="flex w-full h-full border-neutral-800 border flex-col text-center place-content-between">
                    <div class={"flex justify-center items-center font-futurar h-[60%] p-2" + (librarySize ? librarySizeTitleCls : " text-3xl md:text-xl lg:text-3xl")}></div>
                    <div class={"flex justify-center items-center h-[40%] p-2" + (librarySize ? librarySizeAuthorCls : " text-xl md:text-base lg:text-xl")}></div>
                </div>
            </div>
        </div>
    </div>
</div>
{:else}
<div class={"flex justify-center w-full " + cls}>
    <div class={"relative h-0 pb-[130%] w-full shadow-xl shadow-black bg-gradient-to-r from-custom-red-dark to-custom-red-light" + (clickable ? clickableCls : "")}>
        {#if progress == 100}
        <svg class="fill-white opacity-30 absolute h-4 w-4 top-[9%] right-[12%]" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" id="check-circle"><path d="M12,2A10,10,0,1,0,22,12,10,10,0,0,0,12,2Zm4.71,8.71-5,5a1,1,0,0,1-1.42,0l-3-3a1,1,0,1,1,1.42-1.42L11,13.59l4.29-4.3a1,1,0,0,1,1.42,1.42Z"></path></svg>
        {/if}
        <div on:click={onClick}  class={"absolute select-none w-full h-full rounded-sm p-[4%]" }>
            <div class="flex w-full h-full border-neutral-200 border flex-col text-center place-content-between p-[4%]">            
                <div class="flex w-full h-full border-neutral-200 border flex-col text-center place-content-between">
                    <div class={"flex justify-center items-center font-futurar h-[60%] p-2" + (librarySize ? librarySizeTitleCls : " text-3xl md:text-xl lg:text-3xl")}><h1 class="break-words w-full">{title}</h1></div>
                    <div class={"flex justify-center items-center h-[40%] p-2" + (librarySize ? librarySizeAuthorCls : " text-xl md:text-base lg:text-xl")}><h2 lass="break-words w-full">{author}</h2></div>
                </div>
            </div>
        </div>
    </div>
</div>
{/if}