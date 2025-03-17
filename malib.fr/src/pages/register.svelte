<script>
    import Header from "../components/header.svelte";
    import Footer from "../components/footer.svelte";
    import Button from "../components/button.svelte";
    import InputText from "../components/inputText.svelte";
    import Error from "../components/error.svelte";
    import Link from "../components/link.svelte";
    import { api, goTo, registerEmail, isLogged, updateAuthInfo } from "../app.js";
    import * as conf from "../app.json";

    let fEmail;
    let fPassword;
    let apiError;
    let showButtonSpinner = false;

    async function handleForm(){
        if(!fEmail.isValid() || !fPassword.isValid()){
            fEmail.showError();
            fPassword.showError();
        }
        else{
            showButtonSpinner = true;
            let r = await api("/register", "post", {}, {email:fEmail.getValue(), password:fPassword.getValue()}); 

            if(r.status == 200){
                await updateAuthInfo();
                goTo(conf.pages.subscribe.route);
            }
            else if(r.status == 409)
                apiError.show(conf.error.account_exists);
            else if(r.status == 501)
                apiError.show(conf.error.not_yet);
            else if(r.status == 429)
                apiError.show(conf.error.too_many_requests);
            else
                apiError.show(conf.error.default);

            showButtonSpinner = false;
        }
    }
</script>

<div class="min-h-screen flex flex-col">
    <Header hideLoginButton={true}></Header>
    <div class="flex flex-grow flex-col self-center justify-center text-center md:px-6 px-3 max-w-md w-full pt-6 pb-24">
        <h1 class="md:text-4xl text-3xl font-futurar mb-8">{conf.pages.register.title}</h1>
        <h2 class="md:text-xl text-lg mb-4">{conf.register.subtitle}</h2>
        <form class="space-y-4" on:submit|preventDefault>
            <InputText dataType="email" size="big" bind:funcs={fEmail} value={$registerEmail} required={true} />
            <InputText dataType="password" size="big" bind:funcs={fPassword} required={true}/>
            <Error cls="bg-neutral-800 p-3 rounded-lg" bind:funcs={apiError}/>
            <Button on:click={handleForm} size="big" cls="w-full" bind:showSpinner={showButtonSpinner}>{conf.button.next}</Button>
            <div class="flex md:flex-row flex-col justify-center pt-4">
                <Link to={conf.pages.login.route}>{conf.register.already_member}</Link>
            </div>
        </form>
    </div>
</div>
<Footer></Footer>