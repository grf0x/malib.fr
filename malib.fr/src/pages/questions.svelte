<script context="module">
    import * as conf from "../app.json";
    import Header from "../components/header.svelte";
    import Footer from "../components/footer.svelte";
    import QuestionCard from "../components/questionCard.svelte";
</script>

<div class="min-h-screen flex flex-col">
    <Header></Header>
    <div class="flex flex-grow flex-col self-center md:px-6 px-3 max-w-4xl w-full space-y-4 pb-24 pt-6">
        <h1 class="md:text-4xl text-3xl font-futurar mb-8 text-center">{conf.pages.questions.title}</h1>
        {#each conf.questions as q}
        <QuestionCard question={q.question} answer={q.answer}/>
        {/each}
    </div>
</div>
<Footer></Footer>