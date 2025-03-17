<script>
    import { createEventDispatcher } from 'svelte';
    export let rating = null;
    export let disableRating = false;
    export let cls = "w-8 h-8";
    let clsNotSelected = "fill-[#383838] cursor-pointer hover:fill-[#454545] transition ease-in-out duration-300";
    let clsSelected = " fill-custom-red cursor-default";

    const dispatch = createEventDispatcher();
    function onClick(rating){
        if(!disableRating)
            dispatch("click", {rating:rating});
    }
</script>

<div class="flex flex-row space-x-2 justify-center w-full">
    <svg on:click={()=>onClick("D")} class={cls + " " + (rating === "D" ? clsSelected : clsNotSelected)} viewBox="0 0 256 256" id="Flat" xmlns="http://www.w3.org/2000/svg">
        <path d="M128,24A104,104,0,1,0,232,128,104.12041,104.12041,0,0,0,128,24Zm36,72a12,12,0,1,1-12,12A12.0006,12.0006,0,0,1,164,96ZM92,96a12,12,0,1,1-12,12A12.0006,12.0006,0,0,1,92,96Zm81.58545,86.9248a7.99636,7.99636,0,0,1-10.93018-2.91943,40.01579,40.01579,0,0,0-69.30957-.00049,8.00016,8.00016,0,0,1-13.85058-8.01074,56.0156,56.0156,0,0,1,97.00976.00049A7.99915,7.99915,0,0,1,173.58545,182.9248Z"/>
    </svg>
    <svg on:click={()=>onClick("N")} class={cls + " " + (rating === "N" ? clsSelected : clsNotSelected)} viewBox="0 0 256 256" id="Flat" xmlns="http://www.w3.org/2000/svg">
    <path d="M128,24A104,104,0,1,0,232,128,104.12041,104.12041,0,0,0,128,24ZM92,96a12,12,0,1,1-12,12A12.0006,12.0006,0,0,1,92,96Zm76,72H88a8,8,0,0,1,0-16h80a8,8,0,0,1,0,16Zm-4-48a12,12,0,1,1,12-12A12.0006,12.0006,0,0,1,164,120Z"/>
    </svg>
    <svg on:click={()=>onClick("L")} class={cls + " " + (rating === "L" ? clsSelected : clsNotSelected)} viewBox="0 0 256 256" id="Flat" xmlns="http://www.w3.org/2000/svg">
        <path d="M128,24A104,104,0,1,0,232,128,104.12041,104.12041,0,0,0,128,24Zm36,72a12,12,0,1,1-12,12A12.0006,12.0006,0,0,1,164,96ZM92,96a12,12,0,1,1-12,12A12.0006,12.0006,0,0,1,92,96Zm84.50488,60.00293a56.01609,56.01609,0,0,1-97.00976.00049,8.00016,8.00016,0,1,1,13.85058-8.01074,40.01628,40.01628,0,0,0,69.30957-.00049,7.99974,7.99974,0,1,1,13.84961,8.01074Z"/>
    </svg>
</div>
