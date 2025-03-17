<script>
    import * as conf from "../app.json";
    import { onMount } from "svelte";
    import Header from "../components/header.svelte";
    import Footer from "../components/footer.svelte";
    import Button from "../components/button.svelte";
    import Link from "../components/link.svelte";
    import Spinner from "../components/spinner.svelte";
    import KeywordStat from "../components/keywordStat.svelte";
    import EmotionStat from "../components/emotionStat.svelte";
    import NavBookRating from "../components/navBookRating.svelte";
    import ReportIssue from "../components/reportIssue.svelte";
    import { params, goTo, api, removeAccent } from "../app.js";
    let id;
    let ready = false;
    let book;
    let sortedKeywords;
    let sortedEmotions;
    let progress = 75;
    let rating = null;
    let disableRating = false;

    onMount(async ()=>{
        id = $params.id;
        if($params.id){
            let r = await api("/book", "get", {id:id}, {});
            if(r.status == 200){
                book = r.data;
                rating = book.rating;
                sortedKeywords = await sort("keyword");
                sortedEmotions = await sort("emotion");
                ready = true;
            }
            else{
                goTo(conf.pages.new_book.route + "?id=" + id);
            }
        }
        else
            goTo(conf.pages.library.route);
    });

    async function rate(event){
        disableRating = true;
        let newRating = event.detail.rating;
        let r = await api("/rate-book", "post", {}, {book_id:book.id, book_rating:newRating});
        if(r.status == 200){rating = newRating}
        disableRating = false;
    }

    async function sort(type){
        let tmp = {};
        for (const [key, value] of Object.entries(book)) {
            if(key.includes(type))
                tmp[key] = value;
        }
        return Object.keys(tmp).sort(function(a, b) { return tmp[b] - tmp[a];}).slice(0,10);
    }

    function toFileName(str){
        let regex = /[^A-Za-z0-9]/g;
        return removeAccent(str).replaceAll(regex, "_");
    }
</script>


<div class="min-h-screen flex flex-col">
    <Header></Header>
    <div class="flex flex-grow flex-col self-center items-center text-center w-full md:px-6 px-3 pt-2 pb-24 max-w-7xl">
        {#if ready}
        {#if rating == null && book.progress == 100}
        <div class="fixed top-0 left-0 w-[200vw] h-[200vh] -ml-[50vw] -mt-[50vh] overscroll-none bg-black bg-opacity-80 z-[99] flex justify-center items-center">
            <div class="md:p-12 p-6 rounded-lg bg-neutral-900 flex flex-col justify-center items-center">
                <h1 class="w-full text-center md:text-2xl text-xl md:mb-6 mb-4">{conf.book.big_rating}</h1>
                <NavBookRating cls="md:h-24 md:w-24 h-16 w-16" on:click={rate} {rating} {disableRating}/>
            </div>
        </div>
        {/if}
        <div class="bg-neutral-800 md:p-8 p-6 pb-8 pt-8 rounded-lg flex flex-grow md:flex-row flex-col items-center relative">
            <ReportIssue msg={conf.book.report_summary} bookId={book.id} type="summary"/>
            <div class="flex flex-col mb-8 md:w-[35%] w-full md:pt-6 md:pr-6 md:justify-start md:items-start md:border-neutral-700">
                <h1 class="lg:text-5xl md:text-4xl text-3xl md:text-left font-futurar md:mb-0 mb-8 break-normal select-none">{book.title}</h1>
                <div class="flex flex-row-reverse md:flex-col md:border-0 border-y border-neutral-700 py-4 items-center justify-center md:items-start">
                    <h2 class="lg:text-3xl md:text-2xl md:text-left text-xl md:mb-6 md:ml-0 ml-4 break-normal select-none">{book.author_name}</h2>
                    {#if book.img}
                    <img class="md:w-full md:h-full w-16 h-16 md:mb-6 md:mt-2 object-cover rounded-full md:rounded-lg" src={book.img} alt={book.author_name} onerror="this.style.display='none'"/>
                    {/if}
                </div>
                <div class="hidden md:flex">
                    <NavBookRating on:click={rate} {rating} {disableRating}/>
                </div>
            </div>
            <div class="flex flex-col md:w-[65%] items-center md:border-l border-neutral-700 md:pb-6 md:pl-6 md:pt-6">
                <div class="flex flex-col w-full md:mb-4 mb-6">
                    <div class="flex flex-col w-full">
                        <span class="md:text-left text-center font-futurar text-sm select-none">{conf.book.progress_one} {book.progress.toFixed(0)}% {conf.book.progress_two}</span>
                        <div class="flex bg-[#383838] w-full h-3 md:mb-4 mt-4">
                            <div class="bg-gradient-to-r from-custom-red-dark to-custom-red-light select-none" style="width: {book.progress}%"></div>
                        </div>
                    </div>
                </div>
                <p class="text-justify mb-4 md:text-lg text-base select-none">{book.summary}</p>            
                <Button to={conf.pages.reader.route + "?id=" + book.id} cls="w-full mt-4" size="big">{conf.button.read}</Button>
                {#if book.next_book}
                <div class="flex md:flex-row md:space-x-4 flex-col w-full">
                    <Button toExt={conf.book_url + book.id + ".epub?book_title=" + toFileName(book.title)} theme="whiteBox" cls="w-full mt-4" size="big">{conf.button.download}</Button>
                    <Button to={conf.pages.new_book.route + "?id=" + book.next_book} theme="whiteBox" cls="w-full mt-4" size="big">{conf.button.read_next}</Button>
                </div>
                {:else}
                <Button toExt={conf.book_url + book.id + ".epub?book_title=" + toFileName(book.title)} theme="whiteBox" cls="w-full mt-4" size="big">{conf.button.download}</Button> 
                {/if}
                <div class="flex md:hidden mt-8">
                    <NavBookRating on:click={rate} {rating} {disableRating}/>
                </div>
            </div>
        </div>
        <div class="flex w-full mt-8 md:flex-row flex-col">    
            <div class="bg-neutral-800 relative md:p-8 md:pb-10 p-6 pb-8 pt-8 rounded-lg flex items-center self-start flex-col md:order-2 flex-grow md:w-[35%] w-full">
                <ReportIssue msg={conf.book.report_analysis} bookId={book.id} type="emotion"/>
                <h1 class="text-2xl select-none">{conf.book.emotion_analysis}</h1>
                <div class="grid grid-cols-3 gap-8 w-full mt-8 select-none">
                    {#each sortedEmotions as emotion}
                    <EmotionStat name={conf.emotions[emotion]} percent={book[emotion] * 100} light/>
                    {/each}
                </div>
            </div>
            <div class="bg-neutral-800 relative md:p-8 md:pb-10 p-6 pb-8 pt-8 rounded-lg flex items-center self-start flex-col md:mr-8 md:order-1 md:mt-0 mt-8 md:w-[65%] w-full">
                <ReportIssue msg={conf.book.report_analysis} bookId={book.id} type="keyword"/>
                <h1 class="text-2xl select-none">{conf.book.keyword_analysis}</h1>
                <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-10 w-full mt-8">
                    {#each sortedKeywords as keyword}
                    <div class="self-end select-none"><KeywordStat name={conf.keywords[keyword]} percent={book[keyword] * 100} light dynamic={false}/></div>
                    {/each}
                </div>
            </div>
        </div>
        {:else}
        <div class="flex flex-grow w-full justify-center items-center"><Spinner size="big" color="rgb(58,58,58)"/></div>
        {/if}
    </div>
</div>
<Footer></Footer>