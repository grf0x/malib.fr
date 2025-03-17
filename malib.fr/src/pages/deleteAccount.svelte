<script>
    import * as conf from "../app.json";
    import { onMount } from "svelte";
    import Header from "../components/header.svelte";
    import Footer from "../components/footer.svelte";
    import Button from "../components/button.svelte";
    import InputText from "../components/inputText.svelte";
    import Error from "../components/error.svelte";
    import { goTo, api, updateAuthInfo, logout } from "../app.js";
    let apiError;
    let showSpinner;
    let fChecker;

    async function handleForm(){
        if(!fChecker.isValid())
            fChecker.showError();
        else if(fChecker.getValue() !== conf.delete_account.keyword)
            apiError.show(conf.error.invalid_entry + conf.delete_account.keyword);
        else{
            showSpinner = true;
            let r = await api("/delete-account", "post", {}, {});  

            if(r.status == 200){
                logout();
                goTo(conf.pages.confirmation.route + "?type=delac");
            }
            else if(r.status == 401 || r.status == 422)
                apiError.show(conf.error.bad_token);
            else if(r.status == 410)
                apiError.show(conf.error.expired_token);
            else if(r.status == 409)
                apiError.show(conf.error.used_token);
            else
                passwordApiError.show(conf.error.default);
            showSpinner = false;
        }
    }
</script>

<div class="bg-neutral-900 min-h-screen font-futural">
    <div class="min-h-screen flex flex-col">
        <Header></Header>
        <div class="flex flex-grow flex-col justify-center self-center text-center md:px-6 px-3 w-full pb-24 pt-6">
            <div class="flex flex-col md:max-w-md w-full self-center bg-neutral-800 md:p-8 p-6 md:pb-10 pb-8 space-y-4 text-white rounded-xl">
                <h1 class="md:text-2xl text-xl font-futurar">{conf.pages.delete_account.title}</h1>
                <p class="text-justify">{conf.delete_account.warning}</p>
                <p class="text-justify">{conf.delete_account.todo}{conf.delete_account.keyword}{conf.delete_account.todo_next}</p>
                <InputText lower  size="small" bind:funcs={fChecker} required={true}/>
                <Error cls="bg-neutral-700 p-3 rounded-lg" bind:funcs={apiError}/>
                <Button bind:showSpinner on:click={handleForm} size="medium" cls="text-lg">{conf.button.confirm}</Button>
                <Button theme="whiteBox" to={conf.pages.account.route} size="medium" cls="text-lg">{conf.button.cancel}</Button>
            </div>
        </div>
    </div>
    <Footer></Footer>
</div>
