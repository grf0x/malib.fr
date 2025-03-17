<script>
    import * as conf from "../app.json";
    import Header from "../components/header.svelte";
    import Footer from "../components/footer.svelte";
    import Button from "../components/button.svelte";
    import Link from "../components/link.svelte";
    import Book from "../components/bookItem.svelte";
    import KeywordStat from "../components/keywordStat.svelte";
    import Spinner from "../components/spinner.svelte";
    import { onMount } from "svelte";
    import { api, pickFirstBook, goTo, bookCredit, nextCreditDate, params, cacheLibrary, clearParams } from "../app.js";

    const date = { month: "long", day: "numeric" };
    let noMoreBook = false;
    let bookNotFound = false;
    let showButtonSpinnerAdd = false;
    let showButtonSpinnerNi = false;
    let showButtonSpinnerL = false;
    let showButtonSpinnerD = false;
    let recommendationReady = false;
    let book;
    let topKeywords;
    let p = {};

    onMount(async () => {
        if($params.id)
            p.book_id = $params.id;
        await getNewRecommendation();
        recommendationReady = true;
    });

    async function getNewRecommendation(){
        let r = await api("/recommendation", "get", p, {});
        if(r.status == 200){
            book = r.data;      
            let tmp = {};
            for (const [key, value] of Object.entries(book)) {
                if(key.includes("keyword"))
                    tmp[key] = value;
            }
            topKeywords = Object.keys(tmp).sort(function(a, b) { return tmp[b] - tmp[a];}).slice(0,4);
        }
        else if(r.status == 410){
            noMoreBook = true;
        }
        else if(r.status == 404){
            bookNotFound = true;
        }
        else if(r.status == 409){
            goTo(conf.pages.book.route + "?id=" + p.book_id);
        }
    }

    async function clear(){
        clearParams();
        p = {};
    }

    async function passBook(rating){
        if(p){clear()}
        let r = await api("/pass-book", "post", {}, {book_id:book.id, book_rating:rating});  
    }

    async function notInterested(){showButtonSpinnerNi = true; await passBook(null); await getNewRecommendation(); showButtonSpinnerNi = false;}
    async function liked(){showButtonSpinnerL = true; await passBook("L"); await getNewRecommendation(); showButtonSpinnerL = false;}
    async function disliked(){showButtonSpinnerD = true; await passBook("D");await getNewRecommendation(); showButtonSpinnerD = false;}

    async function getNewBook(){
        showButtonSpinnerAdd = true;
        let r = await api("/new-book", "get", {id:book.id}, {});  
        if(r.status == 200){
            $cacheLibrary = null;
            $pickFirstBook = true;
            $bookCredit -= 1;
            goTo(conf.pages.library.route);
        }
        showButtonSpinnerAdd = false;
    }

</script>


<div class="min-h-screen flex flex-col">
    <Header></Header>
    <div class="flex flex-grow md:flex-row flex-col self-center text-center md:items-center w-full md:px-6 px-3 pt-6 pb-24 max-w-6xl">
        {#if noMoreBook || bookNotFound}
        <div class="flex w-full justify-center flex-grow">
            <div class="flex justify-center flex-col md:max-w-md self-center bg-neutral-800 text-white md:p-8 p-6 pt-8 pb-8 space-y-4 rounded-xl"> 
                {#if noMoreBook}
                <h1 class="md:text-3xl text-2xl font-futurar">{conf.new_book.no_more_book_title}</h1>
                <h2 class="md:text-xl text-lg">{conf.new_book.no_more_book_subtitle}</h2>
                {:else}
                <h1 class="md:text-2xl text-2xl font-futurar">{conf.new_book.book_not_found}</h1>
                {/if}
                <Button to={conf.pages.library.route} size="big" cls="w-full">{conf.button.return}</Button>
            </div>
        </div>
        {:else if recommendationReady}
        <div class="flex flex-col px-12 md:order-2 md:mb-0 mb-10 md:w-[45%] md:justify-start md:items-start md:border-neutral-700">
            <Book title="{book.title}" author="{book.author_name}"/>
        </div>
        <div class="flex md:justify-start justify-center items-center md:pb-0 pb-8 md:order-1 md:flex-col md:space-y-4 md:space-x-0 space-x-4">
            {#key book}
                {#each topKeywords as keyword}
                    <KeywordStat name={conf.keywords[keyword]} percent={book[keyword] * 100}/>
                {/each}
            {/key}
        </div>
        <div class="flex flex-col text-justify text-lg md:order-3 md:w-[55%] items-center">
            <p class="mb-4">
                {book.summary}
            </p>
            {#if $bookCredit > 0}
            <Button bind:showSpinner={showButtonSpinnerAdd} on:click={getNewBook} disabled cls="w-full mt-6" size="big">{conf.button.accept}</Button>
            <div class="flex flex-col md:flex-row w-full md:space-x-4">
                <Button bind:showSpinner={showButtonSpinnerNi} on:click={notInterested} theme="whiteBox" cls="w-full mt-4" size="medium">{conf.button.not_interested}</Button>
                <Button bind:showSpinner={showButtonSpinnerL} on:click={liked} theme="whiteBox" cls="w-full mt-4" size="medium">
                    {conf.button.already_read}
                    {#if showButtonSpinnerL == false}
                    <svg class="fill-custom-red w-5 h-5 ml-2" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"  viewBox="0 0 544.582 544.582" style="enable-background:new 0 0 544.582 544.582;"	 xml:space="preserve"><g>	<path d="M448.069,57.839c-72.675-23.562-150.781,15.759-175.721,87.898C247.41,73.522,169.303,34.277,96.628,57.839		C23.111,81.784-16.975,160.885,6.894,234.708c22.95,70.38,235.773,258.876,263.006,258.876		c27.234,0,244.801-188.267,267.751-258.876C561.595,160.732,521.509,81.631,448.069,57.839z"/></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g></svg>
                    {/if}
                </Button>
                <Button bind:showSpinner={showButtonSpinnerD} on:click={disliked} theme="whiteBox" cls="w-full mt-4" size="medium">
                    {conf.button.already_read}
                    {#if showButtonSpinnerD == false}
                    <svg class="fill-neutral-100 w-5 h-5 ml-2" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 512 512" style="enable-background:new 0 0 512 512;" xml:space="preserve"><g>	<g>		<g>			<path d="M117.333,10.667h-64C23.936,10.667,0,34.603,0,64v170.667C0,264.064,23.936,288,53.333,288H160				c5.888,0,10.667-4.779,10.667-10.667V64C170.667,34.603,146.731,10.667,117.333,10.667z"/>			<path d="M512,208c0-18.496-10.603-34.731-26.347-42.667c3.285-6.549,5.013-13.781,5.013-21.333				c0-18.496-10.603-34.752-26.368-42.688c4.864-9.728,6.293-20.928,3.84-32.043C463.36,47.68,443.051,32,419.819,32H224				c-7.232,0-16.405,1.173-25.771,3.285c-5.739,1.301-9.344,6.976-8.064,12.693C191.403,53.632,192,58.859,192,64v213.333				c0,5.739-1.6,11.264-4.736,16.448c-1.835,3.029-2.048,6.763-0.555,9.984l47.957,103.893v72.32c0,3.243,1.472,6.293,3.989,8.341				c0.683,0.555,16.512,13.013,38.677,13.013c24.683,0,64-39.061,64-85.333c0-29.184-10.453-65.515-16.96-85.333h131.755				c28.715,0,53.141-21.248,55.637-48.341c1.387-15.189-3.669-29.824-13.632-40.725C506.901,232.768,512,220.821,512,208z"/>		</g>	</g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g></svg>
                    {/if}
                </Button>
            </div>
            {:else if $nextCreditDate}
            <div class="w-full p-4 border-white border rounded-lg mt-6 text-center"><h4>{conf.new_book.this_book_date + " " + $nextCreditDate.toLocaleDateString(conf.date_format, date) + "."}</h4></div>
            {:else}
            <div class="w-full p-4 border-white border rounded-lg mt-6 text-center"><h4>{conf.new_book.subscribe_book}</h4></div>
            {/if}
        </div>
        {:else}
        <div class="flex w-full justify-center"><Spinner size="big" color="rgb(58,58,58)"/></div>
        {/if}
    </div>
</div>
<Footer></Footer>