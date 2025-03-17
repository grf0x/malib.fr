<script>
    import * as conf from "../app.json";
    import { onMount } from "svelte";
    import Header from "../components/header.svelte";
    import Footer from "../components/footer.svelte";
    import Button from "../components/button.svelte";
    import InputText from "../components/inputText.svelte";
    import Error from "../components/error.svelte";
    import { goTo, api, subCurrentPeriodEnd, updateAuthInfo, isSubCanceled } from "../app.js";
    let apiError;
    let showSpinner;
    const date_day = { year: "numeric", month: "long", day: "numeric"};

    async function handleForm(){
        showSpinner = true;
        let r = await api("/cancel-subscription", "post", {}, {state:true});  

        if(r.status == 200){
            $isSubCanceled = true;
            goTo(conf.pages.account.route);
        }
        else
            apiError.show(conf.error.default);
        showSpinner = false;
    }
</script>

<div class="bg-neutral-900 min-h-screen font-futural">
    <div class="min-h-screen flex flex-col">
        <Header></Header>
        <div class="flex flex-grow flex-col justify-center self-center text-center md:px-6 px-3 w-full pb-24 pt-6">
            <div class="flex flex-col md:max-w-md w-full self-center bg-neutral-800 md:p-8 p-6 md:pb-10 pb-8 space-y-4 text-white rounded-xl">
                <h1 class="md:text-2xl text-xl font-futurar">{conf.unsubscribe.title}</h1>
                <p class="text-justify">{conf.unsubscribe.details_one}<span class="font-extrabold font-futurar">{$subCurrentPeriodEnd.toLocaleDateString(conf.date_format, date_day)}</span>{conf.unsubscribe.details_two}</p>
                <Error cls="bg-neutral-700 p-3 rounded-lg" bind:funcs={apiError}/>
                <Button bind:showSpinner on:click={handleForm} size="medium" cls="text-lg">{conf.button.unsubscribe}</Button>
                <Button theme="whiteBox" to={conf.pages.account.route} size="medium" cls="text-lg">{conf.button.cancel}</Button>
            </div>
        </div>
    </div>
    <Footer></Footer>
</div>
