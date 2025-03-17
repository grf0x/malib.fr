<script>
    import * as conf from "../app.json";
    import Button from "./button.svelte";
    import KeywordStat from "./keywordStat.svelte";
    import { onMount, onDestroy } from 'svelte';
    const startProgress = [251, 251, 251, 251];
    const goalProgress = [215, 218, 220, 225];
    let interval;
    let progress = [...startProgress];
    let time = 0;

    onMount(()=>{play()});
    onDestroy(()=>{flush()});

    function animation(){
        if(progress[0] <= goalProgress[0]){
            if(time > 120)
                play();
        }
        else{
            for(let i = 0; i < 4; i++){
                if(progress[i] > goalProgress[i])
                    progress[i] -= 1;
            }
        }
    }
    function flush(){clearInterval(interval); time=0; progress = [...startProgress]}
    function play(){flush(); interval = window.setInterval(()=>{animation();time += 1;}, 50);}
    function pause(){clearInterval(interval);}
</script>

<div onpagehide={pause()} class="lg:h-[20rem] lg:w-[25.25rem] h-[15rem] w-[18.8rem] select-none tracking-tight">
    <img src="./imgs/desktop.png" alt={conf.pages.new_book.title} class="absolute lg:h-[20rem] lg:w-[25.25rem] h-[15rem] w-[18.8rem]"/>
    <div class="h-full w-full lg:p-[1.05rem] lg:pb-[6rem] p-[0.8rem] pb-[4.55rem]">
        <div class="absolute flex flex-col w-12 space-y-2 mt-[1.55rem] lg:mt-[2rem] lg:ml-[0.8rem] text-neutral-300">
            <div class="flex flex-col justify-center items-center">
                <h2 class="text-[0.5rem]">Historique</h2>
                <svg style="transform: rotate(-90deg); stroke-dasharray: 251; stroke-dashoffset: {progress[0]};" height="20" width="20" class="justify-center items-center">
                    <circle cx="10" cy="10" r="7" stroke-width="3" class="fill-neutral-800 stroke-custom-red" />
                </svg> 
            </div>
            <div class="flex flex-col justify-center items-center">
                <h2 class="text-[0.5rem]">Aventure</h2>
                <svg style="transform: rotate(-90deg); stroke-dasharray: 251; stroke-dashoffset: {progress[1]};" height="20" width="20" class="justify-center items-center">
                    <circle cx="10" cy="10" r="7" stroke-width="3" class="fill-neutral-800 stroke-custom-red" />
                </svg> 
            </div>
            <div class="flex flex-col justify-center items-center">
                <h2 class="text-[0.5rem]">Drame</h2>
                <svg style="transform: rotate(-90deg); stroke-dasharray: 251; stroke-dashoffset: {progress[2]};" height="20" width="20" class="justify-center items-center">
                    <circle cx="10" cy="10" r="7" stroke-width="3" class="fill-neutral-800 stroke-custom-red" />
                </svg> 
            </div>
            <div class="flex lg:visible invisible flex-col justify-center items-center">
                <h2 class="text-[0.5rem]">Suspense</h2>
                <svg style="transform: rotate(-90deg); stroke-dasharray: 251; stroke-dashoffset: {progress[3]};" height="20" width="20" class="justify-center items-center">
                    <circle cx="10" cy="10" r="7" stroke-width="3" class="fill-neutral-800 stroke-custom-red" />
                </svg> 
            </div>
        </div>
        <img class="w-full h-full" src={"imgs/newBook.png"} alt="reader"/>
    </div>
</div>
