<script>
    import * as conf from "../app.json";
    import Header from "../components/header.svelte";
    import Footer from "../components/footer.svelte";
    import Button from "../components/button.svelte";
    import Error from "../components/error.svelte";
    import InputText from "../components/inputText.svelte";
    import Promo from "../components/promo.svelte";
    import Spinner from "../components/spinner.svelte";
    import { onMount, onDestroy } from "svelte";
    import { loadStripe } from "@stripe/stripe-js";
    import { api, isSub, isLogged, getReferrer } from "../app.js";

    let error;
    let showButtonSpinner = false;
    let showBigSpinner = true;
    let stripe;
    let paymentElement;
    let elements;
    let clientSecret;
    let isFirstSub = false;
    let formReady = false;
    let promoCode;
    let invoice;

    onMount(async () => {
        stripe = await loadStripe(conf.stripe_pubkey);
        const referrer = getReferrer();
        let params = {};
        if(referrer)
            params.referrer = referrer;
        if(promoCode)
            params.code = promoCode;
        let r = await api("/subscribe", "post", params, {});
        if(r.status == 200){
            clientSecret = r.data.client_secret;
            invoice = r.data.invoice;
            isFirstSub = r.data.is_first_sub;
            const appearance = {
                theme: "flat", 
                variables: {colorPrimary: "rgb(215,120,120)", colorDanger: "rgb(207,92,92)", borderRadius: "8px"},
                rules:{ ".Input--invalid":{border:"2px solid rgb(215,120,120)"}}
            };
            elements = stripe.elements({appearance, clientSecret:clientSecret});
            paymentElement = elements.create("payment");
            paymentElement.on("ready", () => {formReady=true});
            paymentElement.on("focus", () => {paymentError.hide()});
            paymentElement.on("loaderStart", () => {showBigSpinner=false});
            paymentElement.mount("#formElement");
        }
        else if(r.status == 409)
            error.show(conf.error.already_member);
        else
            error.show(conf.error.default);

        showBigSpinner = false;
    });

    async function handleForm(){
        showButtonSpinner = true;
        const { error } = await stripe.confirmPayment({elements, confirmParams: {return_url: conf.local_url + conf.pages.confirmation.route + "?type=" + (isFirstSub ? "fsub" : "sub")}});
        if(error.type !== "validation_error")
            error.show(error.message);
        showButtonSpinner = false;
    }

</script>

<div class="min-h-screen flex flex-col">
    <Header></Header>
    <div class="flex flex-grow md:flex-row flex-col self-center text-center w-full">
        <div class="flex flex-grow w-full bg-gradient-to-r p-6 from-custom-red-dark to-custom-red-light text-white justify-center items-center">
            <div class="flex flex-col w-full max-w-lg md:my-16 my-12">
                <h1 class="w-full md:text-5xl text-3xl font-futurar md:text-left text-center">{conf.subscribe.title}</h1>
                <h2 class="w-full md:text-2xl text-xl mt-6 md:mb-8 mb-6 md:text-left text-center">{conf.subscribe.subtitle}</h2>
                <!--<Promo invoice={invoice} bind:promoCode/>-->
            </div>
        </div>
        <div class="flex w-full bg-white text-black justify-center items-center">
            <div class="flex flex-col w-full max-w-lg my-8 mx-6">
                <form on:submit|preventDefault={handleForm}>
                    <div id="formElement"></div>
                    <Error cls="mt-4 border-4 border-custom-red text-custom-red-dark font-futurar p-3 mt-6 rounded-lg text-white" bind:funcs={error}/>
                    {#if formReady}
                    <Button showSpinner={showButtonSpinner} size="big" cls="mt-6 w-full">{conf.button.activate_membership}</Button>
                    {/if}
                    {#if showBigSpinner}
                    <div class="flex w-full justify-center p-2 pb-6 flex-col space-y-3 animate-pulse">
                        <div class="flex w-full flex-row space-x-3"><div class="rounded-lg w-full h-16 bg-neutral-200"></div><div class="rounded-lg w-full h-16 bg-neutral-200"></div></div>
                        <div class="flex w-full flex-row space-x-3"><div class="rounded-lg h-3 w-28 bg-neutral-200"></div><div class="w-full"></div></div>
                        <div class="rounded-md w-full h-12 bg-neutral-200"></div>
                        <div class="flex w-full flex-row space-x-3"><div class="flex w-full justify-start"><div class="rounded-lg h-3 w-12 bg-neutral-200"></div></div><div class="flex w-full justify-start"><div class="rounded-lg h-3 w-8 bg-neutral-200"></div></div></div>
                        <div class="flex w-full flex-row space-x-3"><div class="rounded-lg w-full h-12 bg-neutral-200"></div><div class="rounded-lg w-full h-12 bg-neutral-200"></div></div>
                    </div>
                    {/if}
                </form>
            </div>
        </div>
    </div>
</div>
<Footer></Footer>
