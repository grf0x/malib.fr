<script>
    import { createEventDispatcher } from 'svelte';
    import Spinner from "../components/spinner.svelte";
    export let selected = true;
    export let disable = false;
    export let showSpinner = false;
    export let cls = "";
    let clsSelected = " bg-gradient-to-r from-custom-red-dark to-custom-red-light hover:brightness-110 transition ease-in-out duration-300";
    let clsNotSelected = " bg-[#383838] hover:bg-[#454545] transition ease-in-out duration-300";

    const dispatch = createEventDispatcher();
    function onClick(){
        if(!disable)
            dispatch("click");
    }
</script>


<button on:click={onClick} class={"flex items-center p-2 rounded-lg" + (selected ? clsSelected : clsNotSelected) + " " + cls}>
    <div class="flex p-4 pr-6 w-16 justify-center text-white text-2xl">
        {#if showSpinner}
            <Spinner size="small" color="white"/>
        {:else}
            {#if selected}
            <svg class="fill-white" width="20px" height="20px" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 405.272 405.272" style="enable-background:new 0 0 405.272 405.272;"	 xml:space="preserve"><g>	<path d="M393.401,124.425L179.603,338.208c-15.832,15.835-41.514,15.835-57.361,0L11.878,227.836		c-15.838-15.835-15.838-41.52,0-57.358c15.841-15.841,41.521-15.841,57.355-0.006l81.698,81.699L336.037,67.064		c15.841-15.841,41.523-15.829,57.358,0C409.23,82.902,409.23,108.578,393.401,124.425z"/></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g></svg>
            {:else}
            <svg class="fill-white iconify iconify--emojione-monotone" width="20px" height="20px" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" preserveAspectRatio="xMidYMid meet"><path d="M62 10.571L53.429 2L32 23.429L10.571 2L2 10.571L23.429 32L2 53.429L10.571 62L32 40.571L53.429 62L62 53.429L40.571 32z" fill="currentColor"></path></svg>     
            {/if}
        {/if}
    </div>
    <div class="bg-white text-black flex h-full w-full p-4 rounded-lg justify-left items-center text-left"><slot></slot></div>
</button>