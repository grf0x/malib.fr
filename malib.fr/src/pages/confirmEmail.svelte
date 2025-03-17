<script>
    import * as conf from "../app.json";
    import { onMount } from "svelte";
    import Header from "../components/header.svelte";
    import Footer from "../components/footer.svelte";
    import Button from "../components/button.svelte";
    import Link from "../components/link.svelte";
    import { api, params, goTo } from "../app.js";
    let msg;

    onMount(async()=>{
        if($params.t){
            let token = $params.t;
            let r = await api("/email-confirmation", "post", {}, {token:token});  

            if(r.status == 200)
                msg = conf.confirmation.email_confirmed;
            else if(r.status == 401)
                msg = conf.error.bad_token;
            else if(r.status == 409)
                msg = conf.error.used_token;
            else if(r.status == 410)
                msg = conf.error.expired_token;
            else
                msg = conf.error.default;
        }
        else
            goTo(conf.pages.welcome.route);
    });

</script>

<div class="bg-neutral-900 min-h-screen font-futural">
    <div class="min-h-screen flex flex-col">
        <Header></Header>
        <div class="flex flex-grow flex-col justify-center self-center text-center md:px-6 px-3 w-full pb-24 pt-6">
            {#if msg}
            <div class="flex flex-col md:max-w-lg self-center bg-neutral-800 text-white md:p-8 p-6 md:pb-10 pb-8 space-y-4 rounded-xl"> 
                <h1 class="md:text-3xl text-2xl font-futurar">{conf.pages.confirm_email.title}</h1>
                <h2 class="md:text-xl text-lg">{msg}</h2>
                <Button to={conf.pages.login.route} size="big" cls="w-full">{conf.button.continue}</Button>
            </div>
            {/if}
        </div>
    </div>
    <Footer></Footer>
</div>



