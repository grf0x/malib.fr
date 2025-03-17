<script>
    import * as conf from "../app.json";
    import Header from "../components/header.svelte";
    import Footer from "../components/footer.svelte";
    import Book from "../components/bookItem.svelte";
    import InputText from "../components/inputText.svelte";
    import Spinner from "../components/spinner.svelte";
    import { slide } from 'svelte/transition';
    import { api, goTo, settingLibrarySorting, settingReaderFont, settingReaderZoom, settingReaderTheme, cacheLibrary, removeAccent } from "../app.js";
    import { onMount, onDestroy } from "svelte";
    let books = [];
    let bookCount = 0;
    let fSearch;
    let searchBooks = [];
    let loading = true;
    let openSortBy = false;
    let clsSortingSelected = "extra-bold ml-4 cursor-default";
    let clsSortingNotSelected = "extra-bold ml-4 text-white/50 hover:text-white cursor-pointer transition ease-in-out duration-300";

    onMount(async () => {load();});

    async function load(){
        loading = true;
        if($cacheLibrary)
            books = $cacheLibrary;
        else{
            let r = await api("/library", "get", {sort:$settingLibrarySorting}, {});
            books = r.data;
            $cacheLibrary = books;
        }
        bookCount = books.length;
        loading = false;
    }

    function getPlCount(bookCountRow){
        let min = bookCountRow * 3;
        if(bookCount < min)
            return min - bookCount;
        else if(bookCount % bookCountRow == 0)
            return bookCountRow;
        else
            return bookCountRow - (bookCount % bookCountRow);
    }

    async function changeSorting(sorting){
        let settings = {"library_sorting":sorting, "reader_theme":$settingReaderTheme, "reader_zoom":$settingReaderZoom, "reader_font":$settingReaderFont};
        let r = await api("/change-settings", "post", {}, settings);
        if(r.status == 200){
            $settingLibrarySorting = sorting;
            $cacheLibrary = null;
            load();
        }
    }

    function search(){
        let tmp = [];
        let regex = new RegExp(removeAccent(fSearch), "i");
        books.forEach(b => {
            if((removeAccent(b.title).search(regex) != -1) || removeAccent(b.author_name).search(regex) != -1)
                tmp.push(b);
        });
        searchBooks = tmp;
    }

    $:if(fSearch && books){search()};
</script>

<div class="min-h-screen flex flex-col">
    <Header></Header>
    <div class="flex flex-grow flex-col self-center text-center md:px-6 px-3 w-full pb-24">
        <div class="flex flex-col w-full p-3 mb-6 bg-neutral-800 rounded-lg justify-between items-center">
            <div class="flex flex-row w-full justify-between">
                <div class="flex flex-grow items-center flex-row">
                    <span class="font-futurar block md:hidden cursor-pointer" on:click={()=>{openSortBy = !openSortBy}}>{conf.library.sort_by_v2} <span class="text-xs">▼</span></span>
                    <span class="font-futurar hidden md:block cursor-default">{conf.library.sort_by_v1}</span>
                    <span on:click={()=>{changeSorting("ACTIVITY")}} class={($settingLibrarySorting == "ACTIVITY" ? clsSortingSelected : clsSortingNotSelected) + " hidden md:block" }>Date de lecture</span> 
                    <span on:click={()=>{changeSorting("ADDED")}} class={($settingLibrarySorting == "ADDED" ? clsSortingSelected : clsSortingNotSelected) + " hidden md:block" }>Date d'ajout</span> 
                    <span on:click={()=>{changeSorting("AUTHOR")}} class={($settingLibrarySorting == "AUTHOR" ? clsSortingSelected : clsSortingNotSelected) + " hidden md:block" }>Auteur</span> 
                    <span on:click={()=>{changeSorting("TITLE")}} class={($settingLibrarySorting == "TITLE" ? clsSortingSelected : clsSortingNotSelected) + " hidden md:block" }>Titre</span>
                </div>
                <div class="flex flex-row items-center"><InputText dataType="search" cls="w-full" size="vsmall" theme="whiteOpacity" placeholder="Rechercher ({bookCount} {bookCount < 2 ? conf.library.book : conf.library.books})" bind:value={fSearch} checkRegex={false}/></div>
            </div>
            {#if openSortBy}
            <div transition:slide={400} class="flex flex-col md:hidden space-y-4 pb-2 pt-6">
                <span on:click={()=>{changeSorting("ACTIVITY")}} class={$settingLibrarySorting == "ACTIVITY" ? clsSortingSelected : clsSortingNotSelected}>Date de lecture</span> 
                <span on:click={()=>{changeSorting("ADDED")}} class={$settingLibrarySorting == "ADDED" ? clsSortingSelected : clsSortingNotSelected}>Date d'ajout</span> 
                <span on:click={()=>{changeSorting("AUTHOR")}} class={$settingLibrarySorting == "AUTHOR" ? clsSortingSelected : clsSortingNotSelected}>Auteur</span> 
                <span on:click={()=>{changeSorting("TITLE")}} class={$settingLibrarySorting == "TITLE" ? clsSortingSelected : clsSortingNotSelected}>Titre</span>
            </div>
            {/if} 
        </div>
        {#if loading}
        <div class="flex flex-grow w-full justify-center items-center"><Spinner size="big" color="rgb(58,58,58)"/></div>
        {:else}
            {#if fSearch}
                {#if searchBooks.length > 0}
                    <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 2xl:grid-cols-8 gap-6 w-full">
                    {#each searchBooks as b}
                        <Book on:click={()=>{goTo(conf.pages.book.route + "?id=" + b.id)}} clickable librarySize title={b.title} author={b.author_name} progress={b.progress}/>
                    {/each}
                    </div>
                {:else}
                    <div class="flex flex-grow w-full justify-center items-center"><h1 class="text-2xl text-white">{conf.library.no_result}</h1></div>
                {/if}
            {:else}
            <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 2xl:grid-cols-8 gap-4 md:gap-6 w-full">
                {#each books as b}
                    <Book on:click={()=>{goTo(conf.pages.book.route + "?id=" + b.id)}} clickable librarySize title={b.title} author={b.author_name} progress={b.progress}/>
                {/each}
                {#each Array(getPlCount(2)) as _}
                    <Book cls="block md:hidden lg:hidden 2xl:hidden" placeholder/>
                {/each}
                {#each Array(getPlCount(4)) as _}
                    <Book cls="hidden md:block lg:hidden 2xl:hidden" placeholder/>
                {/each}
                {#each Array(getPlCount(6)) as _}
                    <Book cls="hidden md:hidden lg:block 2xl:hidden" placeholder/>
                {/each}
                {#each Array(getPlCount(8)) as _}
                    <Book cls="hidden md:hidden lg:hidden 2xl:block" placeholder/>
                {/each}
            </div>
            {/if}
        {/if}
    </div>
</div>
<Footer></Footer>