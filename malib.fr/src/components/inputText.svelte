<script>
    import * as conf from "../app.json";
    import { onMount } from 'svelte';
    export let showError = false;
    export let required = true;
    export let checkRegex = true;
    export let error = true;
    export let dataType = "";
    export let value = "";
    export let errorBlank = false;
    export let cls = "";
    export let placeholder = " ";
    export let label = conf.label[dataType];
    export let theme = "onGrey";
    export let size = "big";
    export let errorMessage = "";
    export let regex = required ? /.+/ : /.*/;
    export let upper = false;
    export let lower = false;
    export let focus = false;
    let id = "" + (Math.random() * 999999999);
    let themeCls;
    let errorCls;
    let focusCls;
    let noErrorCls;
    let sizeCls;
    let labelCls;
    let input;

    export const funcs = {
        showError(){showError = true},
        hideError(){showError = false},
        isValid(){return !error},
        getValue(){return value},
        setValue(newValue){value = newValue}
    }

    if(theme == "onGrey"){
        errorCls = " border-4 border-custom-red text-black";
        noErrorCls = " border-4 border-neutral-200 text-black";
        labelCls = " pl-[1.30rem]";
    }
    else if(theme == "onWhite"){
        errorCls = " border border-custom-red text-black";
        noErrorCls = " border border-black text-black";
        labelCls = " pl-[1.08rem]";
    }
    else if(theme == "whiteOpacity"){
        focusCls = " px-0 bg-white bg-opacity-5 border-2 border-custom-red text-white";
        noErrorCls = " px-0 bg-white bg-opacity-5 hover:border-opacity-10 border-opacity-5 border-10 border-white border-2 text-white placeholder:text-xs placeholder:text-xs placeholder:text-white/30";
    }

    if(size == "vsmall")
        sizeCls = " text-sm h-8";
    else if(size == "small")
        sizeCls = " text-sm h-12";
    else if(size == "big")
        sizeCls = " text-base h-14 pt-3";
    else if(size == "vbig")
        sizeCls = " text-xl h-16 pt-3";

    if(dataType == "email" && checkRegex){
        errorMessage = conf.error.email;
        regex = /^(?=.{1,254}$)(?:[a-z0-9!#$%&'*+-/=?^_`{|}~]+(?:\.[a-z0-9!#$%&'*+-/=?^_`{|}~]+)*)@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)$/;
    } 
    else if(dataType == "password" && checkRegex){
        errorMessage = conf.error.password;
        regex = /^.{8,128}$/;
    }
    else if(dataType == "area" && checkRegex){
        errorMessage = conf.error.area;
        regex = /^.{1,1000}$/;
    }
    else{
        errorMessage = conf.error.empty_field;
    }
    
    $:if(upper){value = value.toUpperCase()} 
    $:if(lower){value = value.toLowerCase()} 
    $:if(dataType == "email"){value = value.toLowerCase()} 
    $:if(dataType == "referral"){value = value.toUpperCase(); if(value.length > 7){value = value.slice(0,7)}} 
    $:if(regex.test(value)){error = false}else{error = true}
    $:if(dataType == "search" && value != ""){focus = true}else{focus = false}
    $:if(error && showError){themeCls = errorCls}else if(focus){themeCls = focusCls}else{themeCls = noErrorCls}
</script>

<div class={"flex flex-grow flex-col " + cls}>
    {#if dataType == "password"}
    <input on:focus={()=>{showError=false}} bind:this={input} {id} bind:value type="password" placeholder={placeholder} class={"flex flex-grow rounded-lg font-extrabold px-4 outline-none" + sizeCls + themeCls}/>
    {:else if dataType == "area"}
    <textarea on:focus={()=>{showError=false}} bind:this={input} {id} bind:value type="password" placeholder={placeholder} class={"flex flex-grow rounded-lg font-extrabold px-4 outline-none pt-4 pb-4 resize-none" + themeCls}></textarea>
    {:else}
    <input on:focus={()=>{showError=false}} bind:this={input} {id} bind:value type="text" placeholder={placeholder} class={"flex flex-grow rounded-lg font-extrabold px-4 outline-none" + sizeCls + themeCls}/>
    {/if}

    {#if dataType != "area" && size != "small" && size != "vsmall"}
    <label for={id} class={"flex items-center text-neutral-700 absolute duration-200 -mt-[0.35rem]" + labelCls + sizeCls} >{label}</label>
    {/if}

    {#if showError && error}
    <div class="mt-2 text-center">{errorMessage}</div>
    {:else}
        {#if errorBlank}
        <div class="mt-2 md:block hidden">&nbsp;</div>
        {/if}
    {/if}
</div>

<style>
    input:focus-within ~ label,
    input:not(:placeholder-shown) ~ label {
        @apply transform text-xs translate-y-2 h-3 text-black;
    }
</style>