<script>
    import Logo from "./logo.svelte";
    import * as conf from "../app.json";
    import Button from "./button.svelte";
    import Nav from "./nav.svelte";
    import { isLogged, logout, goTo } from "../app.js";
    export let hideLoginButton = false;
    let logoLink = conf.pages.welcome.route;
</script>

<header class="py-3 flex flex-row align-baseline items-center justify-between md:px-6 px-3 select-none">
    <Logo on:click={()=>{goTo(logoLink)}}/>
    {#if hideLoginButton}
    <div></div>  
    {:else}
        {#if $isLogged}
        <Nav/>
        {:else}
        <Button to="{conf.pages.login.route}">{conf.pages.login.title}</Button>
        {/if}
    {/if}
</header>