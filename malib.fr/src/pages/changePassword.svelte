<script>
    import * as conf from "../app.json";
    import Header from "../components/header.svelte";
    import Footer from "../components/footer.svelte";
    import Button from "../components/button.svelte";
    import InputText from "../components/inputText.svelte";
    import Error from "../components/error.svelte";
    import { params, goTo, api } from "../app.js";

    let fOldPassword;
    let fNewPassword;
    let apiError;
    let showSpinner = false;

    async function handleForm(){
        if(!fOldPassword.isValid() || !fNewPassword.isValid()){
            fOldPassword.showError();
            fNewPassword.showError();
        }
        else{
            showSpinner = true;
            let r = await api("/change-password", "post", {}, {old_password:fOldPassword.getValue(), new_password:fNewPassword.getValue()});  

            if(r.status == 200)
                goTo(conf.pages.confirmation.route + "?type=cpass");
            else if(r.status == 401 || r.status == 422)
                apiError.show(conf.error.bad_old_password);
            else if(r.status == 409)
                apiError.show(conf.error.password_identical);
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
                    <h1 class="md:text-2xl text-xl font-futurar">{conf.pages.change_password.title}</h1>
                    <InputText dataType="password" label={conf.label.old_password} size="big" bind:funcs={fOldPassword} checkRegex={false} required={true}/>
                    <InputText dataType="password" label={conf.label.new_password} size="big" bind:funcs={fNewPassword} required={true}/>
                    <Error cls="bg-neutral-700 p-3 rounded-lg" bind:funcs={apiError}/>
                    <Button bind:showSpinner on:click={handleForm} size="medium" cls="w-full text-lg">{conf.button.confirm}</Button>
                </form>
            </div>
        </div>
    </div>
    <Footer></Footer>
</div>
