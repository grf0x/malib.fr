<script>
    import * as conf from "../app.json";
    import { referralCode } from "../app.js";
    import ButtonCopy from "../components/buttonCopy.svelte";
    import Header from "../components/header.svelte";
    import Footer from "../components/footer.svelte";
    let url = conf.local_url + "?ref=" + $referralCode;
</script>

<div class="min-h-screen flex flex-col">
    <Header></Header>
    <div class="flex flex-grow md:flex-row flex-col self-center text-center w-full">
        <div class="flex flex-grow w-full bg-gradient-to-r p-6 from-custom-red-dark to-custom-red-light text-white justify-center items-center">
            <div class="flex flex-col w-full max-w-lg my-16 md:my-32">
                <h1 class="w-full md:text-4xl text-3xl font-futurar md:text-left text-center">{conf.referral.title}</h1>
                <h2 class="w-full md:text-2xl text-xl mt-6 md:text-left text-center">{conf.referral.subtitle}</h2>
            </div>
        </div>
        <div class="flex flex-grow w-full bg-white text-black p-6 justify-center items-center">
            <div class="flex flex-col w-full max-w-lg my-16 md:my-32">
                <h2 class="text-xl mb-4">{conf.referral.share_link}</h2>
                <div class="flex flex-col w-full justify-center">
                    <div class="w-full p-6 border-black border rounded-lg mb-4"><h4 class="text-xl">{url}</h4></div>
                    <ButtonCopy to_copy={url} cls="w-full mb-4">{conf.referral.copy_link}</ButtonCopy>
                    <p>{conf.referral.copy_link_info}</p>
                </div>
            </div>
        </div>
    </div>
</div>
<Footer></Footer>