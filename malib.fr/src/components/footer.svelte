<script>
    import * as conf from "../app.json";
    import Link from "../components/link.svelte";
    let year = new Date().getFullYear();
</script>

<footer class="py-24 text-center text-neutral-500 border-t-4 border-neutral-700">
    <li class="grid md:grid-cols-3 grid-cols-1 text-base select-none">   
        {#each Object.entries(conf.pages) as [key, page]}
            {#if page.footer}
            <ul class="mb-8 md:mb-5">
                <Link to={page.route}>{page.title}</Link>
            </ul> 
            {/if}
        {/each}
    </li>
    <div class="text-sm my-10 select-none">©{year} Malib</div>
</footer>