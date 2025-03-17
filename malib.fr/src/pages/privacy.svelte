<script>
    import * as conf from "../app.json";
    import Header from "../components/header.svelte";
    import Footer from "../components/footer.svelte";
</script>

<div class="min-h-screen flex flex-col">
    <Header></Header>
    <div class="flex flex-grow flex-col self-center md:px-6 px-3 max-w-5xl w-full pb-24 pt-6">
        <h1 class="md:text-4xl text-3xl text-center font-futurar mb-12">{conf.pages.privacy.title}</h1>
        <div>
        <p class="md:text-lg text-base mt-2">{conf.privacy.intro}</p>
        </div>
        {#each conf.privacy.sections as section}
        <div class="mt-8">
            <h2 class="md:text-2xl text-xl font-futurar">{section.title}</h2>
            <p class="md:text-lg text-base mt-2">{section.content}</p>
        </div>
        {/each}
    </div>
</div>
<Footer></Footer>