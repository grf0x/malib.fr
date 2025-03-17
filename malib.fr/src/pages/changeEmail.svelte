<script>
    import * as conf from "../app.json";
    import Header from "../components/header.svelte";
    import Footer from "../components/footer.svelte";
    import Button from "../components/button.svelte";
    import InputText from "../components/inputText.svelte";
    import Error from "../components/error.svelte";
    import { api, goTo, updateAuthInfo, email } from "../app.js";

    let fEmail;
    let apiError;
    let showSpinner = false;

    async function handleForm(){
        if(!fEmail.isValid())
            fEmail.showError();
        else{
            showSpinner = true;
            let new_email = fEmail.getValue();
            let r = await api("/change-email", "post", {}, {new_email:new_email});  

            if(r.status == 200){
                $email = new_email;
                goTo(conf.pages.account.route);
            }
            else if(r.status == 409)
                apiError.show(conf.error.account_exists);
            else if(r.status == 429)
                apiError.show(conf.error.too_many_requests);
            else
                apiError.show(conf.error.default);
            showSpinner = false;
        }
    }
</script>

<div class="bg-neutral-900 min-h-screen font-futural">
    <div class="min-h-screen flex flex-col">
        <Header></Header>
        <div class="flex flex-grow flex-col justify-center self-center text-center md:px-6 px-3 w-full md:pb-36 pt-6 pb-12">
            <div class="flex flex-col md:max-w-md w-full self-center bg-neutral-800 text-white md:p-8 p-6 md:pb-10 pb-8 rounded-xl">
                <form class="space-y-4" on:submit|preventDefault>
                    <h1 class="md:text-2xl text-xl font-futurar">{conf.pages.change_email.title}</h1>
                    <InputText dataType="email" label={conf.label.new_email} size="big" bind:funcs={fEmail} checkRegex={false} required={true}/>
                    <Error cls="bg-neutral-700 p-3 rounded-lg" bind:funcs={apiError}/>
                    <Button bind:showSpinner on:click={handleForm} size="big" cls="w-full text-lg">{conf.button.confirm}</Button>
                </form>
            </div>
        </div>
    </div>
    <Footer></Footer>
</div>
