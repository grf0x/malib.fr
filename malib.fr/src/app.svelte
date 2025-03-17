<script>
    import * as conf from "./app.json";
    import { updateAuthInfo, currentRoute, goTo, clearParams, params, setReferrer, isLogged, isSub, setPref, pickFirstBook, networkFailed, bookCredit } from "./app.js";
    import { onMount } from "svelte";

    import Welcome from "./pages/welcome.svelte";
    import Login from "./pages/login.svelte";
    import Register from "./pages/register.svelte";
    import Subscribe from "./pages/subscribe.svelte";
    import Legal from "./pages/legal.svelte";
    import Contact from "./pages/contact.svelte";
    import Account from "./pages/account.svelte";
    import Referral from "./pages/referral.svelte";
    import DeleteAccount from "./pages/deleteAccount.svelte";
    import PasswordRecovery from "./pages/passwordRecovery.svelte";
    import ChangePassword from "./pages/changePassword.svelte";
    import ChangeEmail from "./pages/changeEmail.svelte";
    import Reader from "./pages/reader.svelte";
    import Unsubscribe from "./pages/unsubscribe.svelte";
    import Confirmation from "./pages/confirmation.svelte";
    import ConfirmEmail from "./pages/confirmEmail.svelte";
    import NewBook from "./pages/newBook.svelte";
    import Library from "./pages/library.svelte";
    import Book from "./pages/book.svelte";
    import Preferences from "./pages/preferences.svelte";
    import Terms from "./pages/terms.svelte";
    import Privacy from "./pages/privacy.svelte";
    import Questions from "./pages/questions.svelte";
    import Redirect from "./pages/redirect.svelte";
    import NetworkFailed from "./pages/networkFailed.svelte";

    import Info from "./components/info.svelte";

    let ready = false;
    let showInfoBeta = false;

    onMount(async()=>{
        await updateAuthInfo();
        ready = true;
        $currentRoute = window.location.pathname;
        if($params.ref !== null){ setReferrer($params.ref); clearParams();};
        //if(localStorage.getItem("hideInfoBeta")){showInfoBeta = false}else{showInfoBeta = true};
    });

    function updateUrl(){
        $currentRoute = window.location.pathname; 
        $params = new Proxy(new URLSearchParams(window.location.search), { get: (searchParams, prop) => searchParams.get(prop)});
    }

    $:onRegister = ($currentRoute === conf.pages.register.route || $currentRoute === conf.pages.subscribe.route);
</script>

{#if showInfoBeta}
<Info title={conf.info.beta.title} content={conf.info.beta.content} showContent={onRegister} on:close={()=>{localStorage.setItem("hideInfoBeta", true)}}/>
{/if}

<svelte:head>
    <link rel="icon" href="favicons/favicon.ico" type="image/x-icon"> 
    <link rel="shortcut icon" href="favicons/favicon.ico" type="image/x-icon"> 
    <link rel="apple-touch-icon" sizes="180x180" href="favicons/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="favicons/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="favicons/favicon-16x16.png">
    <link rel="manifest" href="site.webmanifest">
</svelte:head>

{#if ready}
<div class="bg-neutral-900 min-h-screen font-futural">
    {#if $networkFailed}
    <NetworkFailed/>
    {:else if $currentRoute === conf.pages.welcome.route && !$isLogged}
    <Welcome/>
    {:else if $currentRoute === conf.pages.login.route && !$isLogged}
    <Login/>
    {:else if $currentRoute === conf.pages.register.route && !$isLogged}
    <Register/>
    {:else if $currentRoute === conf.pages.password_recovery.route && !$isLogged}
    <PasswordRecovery/>
    {:else if $currentRoute === conf.pages.subscribe.route && $isLogged && !$isSub}
    <Subscribe/>
    {:else if $currentRoute === conf.pages.account.route && $isLogged}
    <Account/>
    {:else if $currentRoute === conf.pages.referral.route && $isLogged}
    <Referral/>
    {:else if $currentRoute === conf.pages.delete_account.route && $isLogged}
    <DeleteAccount/>
    {:else if $currentRoute === conf.pages.change_password.route && $isLogged}
    <ChangePassword/>
    {:else if $currentRoute === conf.pages.change_email.route && $isLogged}
    <ChangeEmail/>
    {:else if $currentRoute === conf.pages.unsubscribe.route && $isLogged && $isSub}
    <Unsubscribe/>
    {:else if $currentRoute === conf.pages.reader.route && $isLogged && $isSub && $setPref && $pickFirstBook}
    <Reader/>
    {:else if $currentRoute === conf.pages.new_book.route && $isLogged && $isSub && $setPref}
    <NewBook/>
    {:else if $currentRoute === conf.pages.preferences.route && $isLogged && $isSub && !$setPref}
    <Preferences/>
    {:else if $currentRoute === conf.pages.library.route && $isLogged && $isSub && $setPref && $pickFirstBook}
    <Library/>
    {:else if $currentRoute === conf.pages.book.route && $isLogged && $isSub && $setPref && $pickFirstBook}
    <Book/>
    {:else if $currentRoute === conf.pages.confirmation.route}
    <Confirmation/>
    {:else if $currentRoute === conf.pages.confirm_email.route}
    <ConfirmEmail/>
    {:else if $currentRoute === conf.pages.legal.route}
    <Legal/>
    {:else if $currentRoute === conf.pages.contact.route}
    <Contact/>
    {:else if $currentRoute === conf.pages.terms.route}
    <Terms/>
    {:else if $currentRoute === conf.pages.privacy.route}
    <Privacy/>
    {:else if $currentRoute === conf.pages.questions.route}
    <Questions/>
    {:else}
        {#if $isLogged}
            {#if $isSub}
                {#if !$setPref}
                <Redirect page={conf.pages.preferences.route}/>
                {:else if !$pickFirstBook}
                <Redirect page={conf.pages.new_book.route}/>
                {:else}
                <Redirect page={conf.pages.library.route}/>
                {/if}
            {:else}
            <Redirect page={conf.pages.subscribe.route}/>
            {/if}
        {:else}
        <Redirect page={conf.pages.welcome.route}/>
        {/if}
    {/if}
</div>
{/if}
<svelte:window on:popstate={updateUrl}/>





