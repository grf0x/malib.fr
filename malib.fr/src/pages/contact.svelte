<script>
    import * as conf from "../app.json";
    import { onMount } from "svelte";
    import Header from "../components/header.svelte";
    import Footer from "../components/footer.svelte";
    import Button from "../components/button.svelte";
    import Error from "../components/error.svelte";
    import InputText from "../components/inputText.svelte";
    import { api, goTo, email } from "../app.js";

    let fEmail;
    let fMessage;
    let apiError;
    let showButtonSpinner = false;

    onMount(async()=>{
        fEmail.setValue($email);
    });

    async function handleForm(){
        if(!fMessage.isValid() || !fMessage.isValid()){
            fEmail.showError();
            fMessage.showError();
        }
        else{
            showButtonSpinner = true;

            let r = await api("/contact", "post", {}, {email:fEmail.getValue(), msg:fMessage.getValue()});  

            if(r.status == 200)
                goTo(conf.pages.confirmation.route + "?type=okmsg");
            if(r.status == 429)
                apiError.show(conf.error.too_many_requests);
            else
                apiError.show(conf.error.default);

            showButtonSpinner = false;
        }
    }
</script>

<div class="min-h-screen flex flex-col">
    <Header></Header>
    <div class="flex flex-grow flex-col justify-center self-center text-center md:px-6 px-3 max-w-2xl w-full pb-24 pt-6">
        <h1 class="md:text-4xl text-3xl font-futurar mb-8">{conf.pages.contact.title}</h1>
        <form on:submit|preventDefault>
            <InputText dataType="email" size="big" bind:funcs={fEmail} label={conf.label.your_email} required={true}/>
            <InputText dataType="area" cls="mt-4 h-60 text-base" bind:funcs={fMessage} checkRegex={false} required={true}/>
            <Error cls="mt-4 bg-neutral-800 p-3 rounded-lg" bind:funcs={apiError}/>
            <Button on:click={handleForm} showSpinner={showButtonSpinner} size="big" cls="w-full mt-8">{conf.button.send}</Button>
        </form>
    </div>
</div>
<Footer></Footer>