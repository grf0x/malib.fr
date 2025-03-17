<script>
    import * as conf from "../app.json";
    export let options;
    export let name;
    export let multiple;
    export let clsSelector = "flex flex-wrap items-center justify-center";
    export let clsButton = "flex md:text-base text-sm font-semibold m-2 items-center justify-center text-white" + " " + (multiple == true ? "rounded-full px-4 h-16" : "rounded-lg w-64 h-14");
    export let clsSelected = "bg-gradient-to-r from-custom-red-dark to-custom-red-light" + " " + (multiple == true ? "hover:brightness-110" : "");;
    export let clsNotSelected = "bg-neutral-800 hover:brightness-110";
    export let errorMessage = (multiple == true ? conf.error.multiple_choices : conf.error.choice);
    let error = true;
    let showError = false;

    export const funcs = {
        showError(){showError = true},
        hideError(){showError = false},
        isValid(){return !error},
        getOptions(){return options},
        getName(){return name},
        isMultiple(){return multiple}
    }

    function handleClick(option){   
        if(multiple){
            option.selected = !option.selected;
            error = true;
            options.forEach(opt => { 
                if(opt.selected)
                    error = false;
            });
        }
        else{
            options.forEach(opt => { opt.selected = false;});
            option.selected = true;
            error = false;
        }
        options = options;
    }
</script>

<div>
    <div class={clsSelector}>
        {#each options as option}
        <button on:click={()=>{handleClick(option)}} class={clsButton + " " + (option.selected == true ? clsSelected : clsNotSelected)}>{option.label}</button>
        {/each}
    </div>
    {#if showError && error}
    <div class="mt-4 pt-4 text-center border-t-2 border-white">{errorMessage}</div>
    {/if}
</div>




