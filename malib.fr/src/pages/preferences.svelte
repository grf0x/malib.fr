<script>
    import * as conf from "../app.json";
    import Header from "../components/header.svelte";
    import Footer from "../components/footer.svelte";
    import Selector from "../components/selector.svelte";
    import Button from "../components/button.svelte";
    import Error from "../components/error.svelte";
    import { api, goTo, updateAuthInfo } from "../app.js";
    import { onDestroy } from "svelte";

    let showButtonSpinner = false;
    let apiError;
    let pref_form = JSON.parse(JSON.stringify(conf.preferences.form));
    let selectors = Array(pref_form.length);


    async function handleForm(){

        let preferences = {};
        let isFormValid = true;

        selectors.forEach(selector => {
            if(!selector.isValid()){
                isFormValid = false;
                selector.showError(); 
            }
        });

        if(isFormValid){
            selectors.forEach(selector => {
                for(const option of selector.getOptions()){ 
                    if(selector.isMultiple())
                        preferences[option.name] = option.selected;
                    else{
                        if(option.selected){
                            preferences[selector.getName()] = option.value;
                        }   
                    }
                }
            });

            showButtonSpinner = true;
            
            let r = await api("/preferences", "post", {}, preferences);  
            
            if(r.status == 200){
                await updateAuthInfo();
                goTo(conf.pages.new_book.route);
            }
            else
                apiError.show(conf.error.default);

        
            showButtonSpinner = false;
        }
    }
</script>

<div class="min-h-screen flex flex-col">
    <Header></Header>
    <div class="flex flex-grow flex-col self-center items-center text-center max-w-7xl md:px-6 px-3 w-full pt-6 pb-24">
        {#each pref_form as element, id}
            <div class="my-6">
                <h1 class="md:text-2xl text-xl font-futurar mb-4">{element.title}</h1>
                <Selector options={element.options} name={element.name} bind:funcs={selectors[id]} multiple={element.multiple}/>
            </div>
        {/each}
        <Error cls="mt-4 bg-neutral-800 p-3 rounded-lg" bind:funcs={apiError}/>
        <Button bind:showSpinner={showButtonSpinner} on:click={handleForm} cls="max-w-xl w-full mt-10" size="big">{conf.button.next}</Button>
    </div>
</div>
<Footer></Footer>