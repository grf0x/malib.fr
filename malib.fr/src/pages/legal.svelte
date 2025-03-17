<script>
    import * as conf from "../app.json";
    import Header from "../components/header.svelte";
    import Footer from "../components/footer.svelte";
</script>

<div class="min-h-screen flex flex-col">
    <Header></Header>
    <div class="flex flex-grow flex-col self-center text-center md:px-6 px-3 max-w-4xl w-full pb-24 pt-6">
        <h1 class="md:text-4xl text-3xl font-futurar mb-12">{conf.pages.legal.title}</h1>
        <div class="bg-neutral-800 p-8 rounded-lg">
            <h2 class="text-2xl font-futurar mb-6">{conf.legal.about_us}</h2>
            <p>{conf.legal.company_name}</p>
            <p>{conf.legal.company_street}</p>
            <p>{conf.legal.company_city}</p>
            <p class="mt-6">{conf.legal.company_number}</p>
            <p>{conf.legal.email}</p>
        </div>
        <div class="bg-neutral-800 p-8 rounded-lg mt-8">
            <h2 class="text-2xl font-futurar mb-6">{conf.legal.about_provider}</h2>
            <p>{conf.legal.provider_name}</p>
            <p>{conf.legal.provider_street}c</p>
            <p>{conf.legal.provider_city}</p>
        </div>
        <div class="bg-neutral-800 p-8 rounded-lg mt-8">
            <h2 class="text-2xl font-futurar mb-6">{conf.legal.sources_title}</h2>
            {#each conf.legal.sources as source}
                <p><a href={source.link}>{source.name}</a></p>
            {/each}
        </div>
    </div>
</div>
<Footer></Footer>

<style>
    p{
        margin-bottom:0.5rem;
    }
</style>