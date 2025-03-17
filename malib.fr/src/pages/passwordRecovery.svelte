<script>
    import * as conf from "../app.json";
    import { onMount } from "svelte";
    import Header from "../components/header.svelte";
    import Footer from "../components/footer.svelte";
    import Button from "../components/button.svelte";
    import InputText from "../components/inputText.svelte";
    import Error from "../components/error.svelte";
    import { params, goTo, api } from "../app.js";
    let ui;
    let token;

    onMount(async()=>{
        if($params.t)
            token = $params.t;
        if($params.u)
            ui = $params.u;
        else
            goTo("/");
    });

    // SEND
    let fEmail;
    let emailApiError;
    let emailShowButtonSpinner = false;
    
    async function handleFormEmail(){
        if(!fEmail.isValid())
            fEmail.showError();
        else{
            emailShowButtonSpinner = true;
            let r = await api("/password-recovery-email", "get", {send_to:fEmail.getValue()}, {});  

            if(r.status == 200)
                goTo(conf.pages.confirmation.route + "?type=reco");
            else if(r.status == 404 || r.status == 422)
                emailApiError.show(conf.error.user_does_not_exist);
            else
                emailApiError.show(conf.error.default);
            emailShowButtonSpinner = false;
        }
    }

    // RESET
    let fPassword;
    let fConfirmPassword;
    let passwordApiError;
    let passwordShowButtonSpinner = false;
    async function handleFormResetPassword(){
        if(!fPassword.isValid() || !fConfirmPassword.isValid()){
            fPassword.showError();
            fConfirmPassword.showError();
        }
        else if(fPassword.getValue() !== fConfirmPassword.getValue())
            passwordApiError.show(conf.error.passwords_do_not_match);
        else{
            passwordShowButtonSpinner = true;
            let r = await api("/password-recovery", "post", {}, {token:token, new_password:fPassword.getValue()});  

            if(r.status == 200)
                goTo(conf.pages.confirmation.route + "?type=cpass");
            else if(r.status == 401 || r.status == 422)
                passwordApiError.show(conf.error.bad_token);
            else if(r.status == 410)
                passwordApiError.show(conf.error.expired_token);
            else if(r.status == 409)
                passwordApiError.show(conf.error.used_token);
            else
                passwordApiError.show(conf.error.default);
            passwordShowButtonSpinner = false;
        }
    }
</script>

<div class="bg-neutral-900 min-h-screen font-futural">
    <div class="min-h-screen flex flex-col">
        <Header></Header>
        <div class="flex flex-grow flex-col justify-center self-center text-center md:px-6 px-3 w-full md:pb-36 pt-6 pb-12">
            <div class="flex flex-col md:max-w-md w-full self-center bg-neutral-800 text-white p-8 rounded-xl">
                {#if ui === "s"}
                <form on:submit|preventDefault>
                    <h1 class="md:text-2xl text-xl font-futurar">{conf.pages.password_recovery.title}</h1>
                    <InputText dataType="email" cls="mt-8" size="big" bind:funcs={fEmail} required={true}/>
                    <Error cls="mt-4 bg-neutral-700 p-3 rounded-lg" bind:funcs={emailApiError}/>
                    <Button bind:showSpinner={emailShowButtonSpinner} on:click={handleFormEmail} size="big" cls="mt-6 mb-3 w-full text-lg">{conf.button.reset}</Button>
                </form>
                {:else if ui === "r"}
                <form on:submit|preventDefault>
                    <h1 class="md:text-2xl text-xl font-futurar">{conf.password_recovery.reset_title}</h1>
                    <InputText dataType="password" cls="mt-8" size="big" bind:funcs={fPassword} required={true}/>
                    <InputText dataType="password" label={conf.label.confirm_password} cls="mt-4" size="big" bind:funcs={fConfirmPassword} required={true}/>
                    <Error cls="mt-4 bg-neutral-700 p-3 rounded-lg" bind:funcs={passwordApiError}/>
                    <Button bind:showSpinner={passwordShowButtonSpinner} on:click={handleFormResetPassword} size="big" cls="mt-6 mb-3 w-full text-lg">{conf.button.confirm}</Button>
                    </form>
                {/if}
            </div>
        </div>
    </div>
    <Footer></Footer>
</div>
