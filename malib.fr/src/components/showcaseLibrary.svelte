<script>
    import * as conf from "../app.json";
    import { onMount, onDestroy } from 'svelte';
    import { fade } from "svelte/transition";
    import Button from "../components/button.svelte";
    let box;
    let speed = 4;
    let interval;
    let scroll;
    let openBook;
    let showCursor;
    let time;
    let progress = 37;

    onMount(()=>{play()});
    onDestroy(()=>{flush()});

    function animation(){ 
        if(time < 120)
            scrollLibrary();
        else if(time == 200)
            showCursor = true;
        else if(time == 220)
            showCursor = false;
        else if(time == 240)
            openBook = true;
        else if(time > 600)
            play();
    }

    function scrollLibrary(){
        scroll += speed;
        box.scroll(0, scroll);
    }

    function flush(){clearInterval(interval); time=0; scroll=0; openBook=false; showCursor=false;}
    function play(){flush(); interval = window.setInterval(()=>{animation();time += 1;}, 10);}
    function pause(){clearInterval(interval);}
</script>

<div onpagehide={pause()} class="md:mt-0 mt-10 max-h-96 h-96 max-w-52 w-52 py-4 px-5 select-none">
    <img src="./imgs/mobile.png" class="absolute h-96 -my-3 -mx-5 z-50" alt=""/>
    {#if showCursor}
    <div transition:fade="{{duration:200}}" class="absolute mt-[9.5rem] ml-9 h-6 w-6 bg-white bg-opacity-50 rounded-full"></div>
    {/if}
    {#if openBook}
    <div in:fade="{{duration:500}}" class="h-full rounded-3xl bg-neutral-900 pt-4 pl-1">
        <h1 class="text-center text-lg mt-2 font-extrabold">{conf.welcome.library.selected_book.title}</h1>
        <div class="flex justify-center items-center border-y border-neutral-800 py-2 my-2">
            <img src="./imgs/go.jpg" alt="George Orwell" class="rounded-full h-5">
            <h2 class="text-xs pl-2">{conf.welcome.library.selected_book.author}</h2>
        </div>
        <div class="flex flex-col w-full py-1 px-3">
            <span class="text-center text-[0.5rem]">{conf.book.progress_one} {progress}% {conf.book.progress_two}</span>
            <div class="flex bg-neutral-700 w-full h-1 mt-2">
                <div class="bg-gradient-to-r from-custom-red-dark to-custom-red-light" style={"width:" + progress + "%;"}></div>
            </div>
        </div>
        <p class="text-justify text-[0.56rem] py-3 px-3">{conf.welcome.library.selected_book.summary}</p>
        <div class="px-3"><Button size="tiny" cls="w-full font-semibold">{conf.button.read}</Button></div>
    </div>
    {/if}
    {#if !openBook}
    <div in:fade="{{duration:500}}" bind:this={box} class="h-full bg-neutral-900 rounded-3xl justify-center overflow-hidden grid grid-cols-2 row pl-3 pr-2 gap-x-4 gap-y-3 border-neutral-700 border-2">
        {#each Array(3) as _} 
            {#each conf.welcome.library.books as book}     
            <div class="flex bg-gradient-to-r from-custom-red-dark to-custom-red-light transition ease-in-out duration-300 w-full aspect-[3/4] rounded-sm p-[4%] cursor-pointer shadow-xl shadow-black">
                <div class="flex w-full h-full border-neutral-200 border flex-col text-center place-content-between p-[4%]">            
                    <div class="flex w-full h-full border-neutral-200 border flex-col text-center place-content-between">
                        <h4 class="flex justify-center items-center text-[0.6rem] font-futurar h-[50%] p-1">{book.title}</h4>
                        <h5 class="flex justify-center items-center text-[0.6rem] h-[50%] p-1">{book.author}</h5>
                    </div>
                </div>
            </div>
            {/each}
        {/each}
    </div>
    {/if}
</div>
