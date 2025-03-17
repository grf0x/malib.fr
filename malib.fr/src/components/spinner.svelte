<script>
    export let size = "small";
    export let color = "white";
    let clsSize = " h-4 w-4";

    if(size == "tiny")
        clsSize = " h-2 w-2"
    else if(size == "small")
        clsSize = " h-4 w-4"
    else if(size == "small_medium")
        clsSize = " h-6 w-6"
    else if(size == "medium")
        clsSize = " h-12 w-12"
    else if(size == "medium_button")
        clsSize = " h-8 w-8"
    else if(size == "big_button")
        clsSize = " h-12 w-12"
    else if(size == "big")
        clsSize = " h-20 w-20"
</script>

<svg fill={color} class={"animate-spin" + clsSize} viewBox="0 0 50 50" xmlns="http://www.w3.org/2000/svg"><circle cx="25" cy="10" r="2"/><circle opacity=".3" cx="25" cy="40" r="2"/><circle opacity=".3" cx="32.5" cy="12" r="2"/><circle opacity=".3" cx="17.5" cy="38" r="2"/><circle opacity=".93" cx="17.5" cy="12" r="2"/><circle opacity=".3" cx="32.5" cy="38" r="2"/><circle opacity=".65" cx="10" cy="25" r="2"/><circle opacity=".3" cx="40" cy="25" r="2"/><circle opacity=".86" cx="12" cy="17.5" r="2"/><circle opacity=".3" cx="38" cy="32.5" r="2"/><circle opacity=".44" cx="12" cy="32.5" r="2"/><circle opacity=".3" cx="38" cy="17.5" r="2"/></svg>

