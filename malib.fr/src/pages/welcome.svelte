<script>
    import * as conf from "../app.json";
    import Header from "../components/header.svelte";
    import Footer from "../components/footer.svelte";
    import Button from "../components/button.svelte";
    import InputText from "../components/inputText.svelte";
    import QuestionCard from "../components/questionCard.svelte";
    import ShowcaseLibrary from "../components/showcaseLibrary.svelte";
    import ShowcaseNewBook from "../components/showcaseNewBook.svelte";
    import ShowcaseReader from "../components/showcaseReader.svelte";
    import { registerEmail, goTo } from "../app.js"
    let fEmailTop;
    let fEmailBottom;
    let ShowError = false;

    function handleForm(form){
        let fEmail = (form == "top" ? fEmailTop : fEmailBottom)
        if(!fEmail.isValid())
            fEmail.showError()
        else{
            $registerEmail = fEmail.getValue();
            goTo(conf.pages.register.route);
        }
    }
</script>

<div class="min-h-95 flex flex-col bg-welcome bg-center">
    <Header></Header>
    <div class="flex flex-grow flex-col justify-center text-center md:px-6 px-3 pt-12 md:pb-28 pb-24 md:max-w-5xl self-center">
        <h1 class="font-futurar md:text-5xl text-4xl">{conf.welcome.first_main_title}</h1>
        <h2 class="md:text-2xl text-xl mt-4 md:px-28">{conf.welcome.second_main_title}</h2>
        <p class="md:text-lg text-base mt-10">{conf.welcome.third_main_title}</p>
        <form on:submit|preventDefault class="mt-3 flex items-start md:flex-row flex-col md:space-x-3 md:space-y-0 space-y-3 md:mx-40">
            <InputText cls="md:w-auto w-full" dataType="email" size="vbig" bind:funcs={fEmailTop} errorBlank={true}/>
            <Button on:click={()=>{handleForm("top")}} cls="md:w-auto w-full" size="vbig">{conf.pages.register.title}</Button>
        </form>
    </div>
</div>

<div class="py-24 border-t-4 border-neutral-700 md:px-28 px-3 grid md:grid-cols-2 grid-cols-1">
    <div class="flex flex-col md:text-left text-center justify-center">
        <h1 class="md:text-5xl text-3xl font-futurar">{conf.welcome.new_book.title}</h1>
        <h2 class="md:text-2xl text-xl pt-6">{conf.welcome.new_book.subtitle}</h2>
    </div>
    <div class="flex justify-center items-center md:pl-20 md:pt-0 pt-10">
        <ShowcaseNewBook/>
    </div>
</div>

<div class="md:py-16 py-24 border-t-4 border-neutral-700 md:px-28 px-3 grid md:grid-cols-2 grid-cols-1">
    <div class="flex flex-col md:text-left text-center justify-center">
        <h1 class="md:text-5xl text-3xl font-futurar">{conf.welcome.library.title}</h1>
        <h2 class="md:text-2xl text-xl pt-6">{conf.welcome.library.subtitle}</h2>
    </div>
    <div class="flex justify-center md:order-first md:pr-20">
        <ShowcaseLibrary/>
    </div>
</div>

<div class="py-24 border-t-4 border-neutral-700 md:px-28 px-3 grid md:grid-cols-2 grid-cols-1">
    <div class="flex flex-col md:text-left text-center justify-center">
        <h1 class="md:text-5xl text-3xl font-futurar">{conf.welcome.reader.title}</h1>
        <h2 class="md:text-2xl text-xl pt-6">{conf.welcome.reader.subtitle}</h2>
    </div>
    <div class="flex justify-center md:pl-20 md:pt-0 pt-10">
        <ShowcaseReader/>
    </div>
</div>

<div class="flex py-20 border-t-4 border-neutral-700 px-3 justify-center">
    <div class="max-w-3xl w-full space-y-4">
        <h1 class="md:text-5xl text-3xl font-futurar text-center pb-8">{conf.pages.questions.title}</h1>
        {#each conf.questions as q}
            {#if q.welcome_page}
            <QuestionCard question={q.question} answer={q.answer}/>
            {/if}
        {/each}
    </div>
</div>

<div class="pt-20 pb-24 border-t-4 border-neutral-700 px-3">
    <h2 class="text-2xl pb-4 text-center">{conf.welcome.third_main_title}</h2>
    <form on:submit|preventDefault class="mt-3 flex items-start flex-grow md:flex-row flex-col md:space-x-3 md:space-y-0 space-y-3 md:max-w-2xl mx-auto">
        <InputText cls="md:w-auto w-full" dataType="email" size="vbig" bind:funcs={fEmailBottom}/>
        <Button cls="md:w-auto w-full" on:click={()=>{handleForm("bottom")}} size="vbig">{conf.pages.register.title}</Button>
    </form> 
</div>

<Footer></Footer>

