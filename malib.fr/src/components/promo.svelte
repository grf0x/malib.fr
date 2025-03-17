<script>
    import * as conf from "../app.json";
    import { createEventDispatcher } from 'svelte';
    import { api } from "../app.js";
    import Spinner from "../components/spinner.svelte";
    export let promoCode = null;
    let value;
    let input;
    let valid = false;
    let focus = false;
    let promoDetails;
    let showSpinner;
    let timeOutCheck;

    function newPromoCode(){
        clearTimeout(timeOutCheck);
        if(value){
            focus = true;
            timeOutCheck = setTimeout(()=> {checkPromo()},2000);
            showSpinner = true;
        }
        else
            focus = false;
    }

    async function checkPromo(){
        let r = await api("/promo-code-validation", "get", {"code":value.toUpperCase()}, {});
        if(r.status == 200){
            valid = true;
            promoDetails = r.data.description;
            promoCode = r.data.code;
        }
        else if(r.status == 409){
            valid = false;
            promoDetails = conf.subscribe.already_discount;
            promoCode = null;
        }
        else if(r.status == 403){
            valid = false;
            promoDetails = conf.subscribe.not_eligible;
            promoCode = null;
        }
        else if(r.status == 429){
            valid = false;
            promoDetails = conf.error.too_many_requests;
            promoCode = null;
        }else{
            valid = false;
            promoDetails = conf.subscribe.invalid_promo;
            promoCode = null;
        }
        showSpinner = false;
    }

    $:value, newPromoCode();
    $:if(!value){promoCode = null};
</script>
<div class="w-full flex flex-col md:justify-start justify-center">
    <div class="flex flex-row md:justify-start justify-center">
        <input bind:value type="text" placeholder={conf.subscribe.promo} class="border-2 border-white bg-white bg-opacity-25 text-white placeholder-white p-2 font-sans font-bold rounded-md placeholder:capitalize placeholder:font-futural placeholder:font-normal uppercase focus:placeholder-transparent outline-none w-40 h-12"/>
        {#if focus}
        <div class="flex w-12 h-12 ml-2 rounded-md border-2 border-white justify-center items-center">
            {#if showSpinner}
                <Spinner size="small_medium" color="white"/>
            {:else}
                {#if valid}
                <svg class="fill-white" width="20px" height="20px" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 405.272 405.272" style="enable-background:new 0 0 405.272 405.272;"	 xml:space="preserve"><g>	<path d="M393.401,124.425L179.603,338.208c-15.832,15.835-41.514,15.835-57.361,0L11.878,227.836		c-15.838-15.835-15.838-41.52,0-57.358c15.841-15.841,41.521-15.841,57.355-0.006l81.698,81.699L336.037,67.064		c15.841-15.841,41.523-15.829,57.358,0C409.23,82.902,409.23,108.578,393.401,124.425z"/></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g></svg>
                {:else}
                <svg class="fill-white iconify iconify--emojione-monotone" width="20px" height="20px" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" preserveAspectRatio="xMidYMid meet"><path d="M62 10.571L53.429 2L32 23.429L10.571 2L2 10.571L23.429 32L2 53.429L10.571 62L32 40.571L53.429 62L62 53.429L40.571 32z" fill="currentColor"></path></svg>     
                {/if}
            {/if}
        </div>
        {/if}
    </div>
    {#if focus && !showSpinner && promoDetails}
        <span class="text-white text-xs md:text-left text-center mt-2">{promoDetails}</span>
    {:else}
    <span class="text-white text-xs md:text-left text-center mt-2">&nbsp;</span>
    {/if}
</div>


