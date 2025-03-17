<script>
    export let theme;
    export let size;
    export let min = 80;
    export let max = 300;
    let minusEnable;
    let plusEnable;

    function increase(){
        if(plusEnable)
            size += 10;
    }

    function decrease(){
        if(minusEnable)
            size -= 10;
    }

    $:minusEnable = (size > min)
    $:plusEnable = (size < max)
</script>

<div class="flex h-16 justify-center items-center">
    <div on:click={decrease} style="color:{theme.background};" class="flex justify-center items-center font-serif w-full h-full text-xl" class:disabled={!minusEnable} class:cursor-pointer={minusEnable} class:cursor-default={!minusEnable}>
        A<div class="flex ml-[-0.1rem] mb-[0.5rem]">-</div>
    </div>
    <hr style="border-left:1px solid {theme.background}">
    <div on:click={increase} style="color:{theme.background};" class="flex justify-center items-center font-serif w-full h-full text-3xl" class:disabled={!plusEnable} class:cursor-pointer={plusEnable} class:cursor-default={!plusEnable}>
        A<div class="flex ml-[-0.1rem] mb-[0.5rem]">+</div>
    </div>
</div>

<style>
    hr{
        height:100%;
        width:1px; 
    }
    .disabled{
        opacity: 0.5;
    }
</style>