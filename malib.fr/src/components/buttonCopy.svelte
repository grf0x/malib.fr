<script>
    import * as conf from "../app.json";
    export let to_copy;
    export let confirm_copy = false;
    export let cls = "";
    let clsNormal = " bg-gradient-to-r from-custom-red-dark to-custom-red-light hover:brightness-110 transition ease-in-out duration-300";
    let clsConfirm = " bg-neutral-900";

    function copy(){
        confirm_copy = true;
        let textArea = document.createElement("textarea");
        textArea.value = to_copy;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand("copy");
        document.body.removeChild(textArea);
        setTimeout(() => {
            confirm_copy = false;
        }, 1500);
    }
</script>

<button on:click={copy} disabled={confirm_copy} class={"flex text-white font-futurar text-xl justify-center items-center p-2 rounded-lg h-20" + (confirm_copy ? clsConfirm : clsNormal) + " " + cls}>
    {#if confirm_copy}
    {conf.button.confirm_copy}
    {:else}
    <slot></slot>
    {/if}
</button>