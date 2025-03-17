<script>
    import { onMount } from "svelte";
    export let name;
    export let percent;
    export let light = false;
    export let dynamic = true;
    let range = 251 - 125;
    let to = Math.floor((251 - ((range / 100) * percent)));
    let progress = 251;

    onMount(()=>{
        if(dynamic){
                let interval = setInterval(() => {
                if(progress > to)
                    progress -= 1;
                else
                    clearInterval(interval);
            }, 10);
        }
        else{
            progress = to;
        }
    });
</script>

<div class="flex flex-col md:justify-center justify-end items-center self-stretch flex-1">
    <div class="flex items-center text-center mb-2"><h2>{name}</h2></div>
    <svg style="transform: rotate(-90deg); stroke-dasharray: 251; stroke-dashoffset: {progress};" height="60" width="60" class="justify-center items-center">
        <circle cx="30" cy="30" r="20" stroke-width="6" class={light ? "fill-[#383838] stroke-custom-red" : "fill-neutral-800 stroke-custom-red"} />
    </svg> 
</div>
