<script>
    import * as conf from "../app.json";
    import { onMount } from "svelte";
    import Header from "../components/header.svelte";
    import Footer from "../components/footer.svelte";
    import Button from "../components/button.svelte";
    import Link from "../components/link.svelte";
    import { params, clearParams, goTo, isSub, updateAuthInfo } from "../app.js";
    let type;
    let showButtonSpinner = false;

    onMount(async()=>{
        if($params.type){
            if($params.redirect_status)
                clearParams("?type=" + $params.type); 
            type = $params.type;
        } 
        else
            goTo(conf.pages.welcome.route);
    });

    async function goToPref(){
        showButtonSpinner = true;
        
        await updateAuthInfo();
        goTo(conf.pages.preferences.route);

        showButtonSpinner = false;
    }
</script>

<div class="bg-neutral-900 min-h-screen font-futural">
    <div class="min-h-screen flex flex-col">
        <Header></Header>
        <div class="flex flex-grow flex-col justify-center self-center text-center md:px-6 px-3 w-full pb-24 pt-6">
            <div class="flex flex-col md:max-w-md self-center bg-neutral-800 text-white md:p-8 p-6 md:pb-10 pb-8 space-y-4 rounded-xl"> 
            {#if type === "fsub"}
                <h1 class="md:text-3xl text-2xl font-futurar">{conf.confirmation.subscribe_title}</h1>
                <h2 class="md:text-xl text-lg">{conf.confirmation.first_subscribe}</h2>
                <Button bind:showSpinner={showButtonSpinner} on:click={goToPref} size="big" cls="w-full">{conf.button.next}</Button>
            {:else if type === "sub"}
                <h1 class="md:text-3xl text-2xl font-futurar">{conf.confirmation.subscribe_title}</h1>
                <h2 class="md:text-xl text-lg">{conf.confirmation.not_first_subscribe}</h2>
                <Button bind:showSpinner={showButtonSpinner} on:click={goToPref} size="big" cls="w-full">{conf.button.next}</Button>
            {:else if type === "cpass"}
                <h1 class="md:text-3xl text-2xl font-futurar">{conf.pages.change_password.title}</h1>
                <h2 class="md:text-xl text-lg">{conf.confirmation.change_password}</h2>
                <Button to={conf.pages.account.route} size="big" cls="w-full">{conf.button.continue}</Button>
            {:else if type === "okmsg"}
                <h1 class="md:text-3xl text-2xl font-futurar">{conf.pages.contact.title}</h1>
                <h2 class="md:text-xl text-lg">{conf.confirmation.contact}</h2>
                <Button to={conf.pages.library.route} size="big" cls="w-full">{conf.button.continue}</Button>
            {:else if type === "reco"}
                <h1 class="md:text-3xl text-2xl font-futurar">{conf.confirmation.password_recovery_title}</h1>
                <p class="text-lg">{conf.confirmation.password_recovery_details}</p>
                <p class="text-lg">{conf.confirmation.password_recovery_no_email_access} <Link to={conf.pages.contact.route} cls="underline">{conf.confirmation.password_recovery_no_email_access_link}</Link>.</p>
            {:else if type === "delac"}
                <h1 class="md:text-3xl text-2xl font-futurar">{conf.confirmation.delete_account}</h1>
                <p class="text-lg">{conf.delete_account.good_bye}</p>
            {/if}
            </div>
        </div>
    </div>
    <Footer></Footer>
</div>



