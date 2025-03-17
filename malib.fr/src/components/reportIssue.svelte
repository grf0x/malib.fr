<script>
    import * as conf from "../app.json";
    import Button from "./button.svelte";
    import Spinner from "../components/spinner.svelte";
    import { clickOutside, api } from "../app.js";
    export let msg;
    export let bookId;
    export let type;
    let open = false;
    let showSpinner = false;
    let reportSent = false;

    async function report(reportType){
        showSpinner = true;
        let r = await api("/report", "post", {}, {book_id:bookId, report_type:reportType});  
        if(r.status == 200){
            showSpinner = false;
            reportSent = true;
        }else{
            showSpinner = false;
        }
    }
</script>

<div use:clickOutside={()=>{open = false}}>

    <div class="flex w-full">
        <svg  on:click={()=>{open = !open;}} class={"absolute top-3 right-3 z-40 h-5 w-5 cursor-pointer transition ease-in-out duration-300 " + (open ? "fill-neutral-600" : "fill-[#383838] hover:fill-[#454545]")} viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg">
            <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8 4a.905.905 0 0 0-.9.995l.35 3.507a.552.552 0 0 0 1.1 0l.35-3.507A.905.905 0 0 0 8 4zm.002 6a1 1 0 1 0 0 2 1 1 0 0 0 0-2z"/>
        </svg>
        {#if open}
        <div class="flex flex-col absolute top-2 right-2 rounded-lg z-30 bg-white text-black text-sm w-72">
            <div class={"flex flex-col p-5 " + ((showSpinner || reportSent) ? "invisible" : "visible")}>
                {msg}
                {#if type == "summary"}
                <Button on:click={()=>{report(type.toUpperCase() + "_TYPO")}} cls="mt-3" showSpinner={(showSpinner || reportSent)} size="small">{conf.report_typo}</Button>
                {/if}
                <Button on:click={()=>{report(type.toUpperCase() + "_ERROR")}} cls="mt-3" showSpinner={(showSpinner || reportSent)} size="small">{conf.report_error}</Button>
            </div>
            {#if showSpinner}
            <div class="absolute w-full h-full justify-center items-center flex p-5"><Spinner size="big" color="#525252"/></div>
            {:else if reportSent}
            <div class="absolute w-full h-full justify-center items-center flex flex-col p-5">
                <svg class="fill-neutral-600 h-24 w-24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12,2A10,10,0,1,0,22,12,10,10,0,0,0,12,2Zm4.71,8.71-5,5a1,1,0,0,1-1.42,0l-3-3a1,1,0,1,1,1.42-1.42L11,13.59l4.29-4.3a1,1,0,0,1,1.42,1.42Z"></path></svg>
                <p class="mt-2 mb-3">{conf.report_sent}</p>
            </div>
            {/if}
        </div>
        {/if}
    </div>

</div>
