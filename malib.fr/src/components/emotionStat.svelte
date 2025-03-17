<script>
    import { onMount } from "svelte";
    export let name;
    export let percent;
</script>

<div class="flex flex-col md:justify-center justify-end items-center self-stretch flex-1">
    <div class="flex items-center text-center mb-4"><h2>{name}</h2></div>
    <div class="w-4 h-14 bg-[#383838]">
        <div class="w-4" style="height: {100 - percent}%"></div>
        <div class="w-4 bg-custom-red self-end end" style="height: {percent}%">
        </div>
    </div>
</div>
