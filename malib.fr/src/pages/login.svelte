<script>
    import Header from "../components/header.svelte";
    import Footer from "../components/footer.svelte";
    import Button from "../components/button.svelte";
    import Error from "../components/error.svelte";
    import InputText from "../components/inputText.svelte";
    import Link from "../components/link.svelte";
    import * as conf from "../app.json";
    import { api, goTo, updateAuthInfo } from "../app.js";
    
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
            let r = await api("/login", "post", {}, {email:fEmail.getValue(), password:fPassword.getValue()});  

            if(r.status == 200){
                await updateAuthInfo();
                goTo(conf.pages.library.route);
            }
            else if(r.status == 401 || r.status == 422)
                apiError.show(conf.error.bad_credentials);
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
        <h1 class="md:text-4xl text-3xl font-futurar mb-8">{conf.pages.login.title}</h1>
        <form class="space-y-4" on:submit|preventDefault>
            <InputText dataType="email" size="big" bind:funcs={fEmail} required={true}/>
            <InputText dataType="password" size="big" bind:funcs={fPassword} checkRegex={false} required={true}/>
            <Error cls="bg-neutral-800 p-3 rounded-lg" bind:funcs={apiError}/>
            <Button bind:showSpinner={showButtonSpinner} on:click={handleForm} size="big" cls="w-full">{conf.button.confirm}</Button>
            <div class="flex flex-col justify-between pt-4">
                <Link to="/">{conf.login.first_visit}</Link>
                <Link to={conf.pages.password_recovery.route + "?u=s"} cls="mt-4">{conf.login.forgotten_password}</Link>
            </div>
        </form>
    </div>
</div>
<Footer></Footer>