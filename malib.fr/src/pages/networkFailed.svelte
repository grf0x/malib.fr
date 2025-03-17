<script>
    import * as conf from "../app.json";
    import Header from "../components/header.svelte";
    import Footer from "../components/footer.svelte";
</script>

<div class="min-h-screen flex flex-col">
    <Header hideLoginButton="true"></Header>
    <div class="flex flex-grow flex-col self-center text-center md:px-6 px-3 max-w-4xl w-full pb-24 pt-6">
        <div class="flex flex-grow flex-col justify-center self-center text-center px-6 w-full pb-24 pt-6">
            <div class="flex flex-col md:max-w-md self-center bg-neutral-800 text-white p-8 space-y-4 rounded-xl"> 
                <h1 class="text-3xl">{conf.network_failed}</h1>
                <p class="text-lg">{conf.network_failed_instructions}</p>
            </div>
        </div>
    </div>
</div>

