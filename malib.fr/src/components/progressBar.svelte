<script>
    import * as conf from "../app.json";
    export let totalPages = 400;
    export let progressPages = 150;
    
    $: progress = Math.trunc(progressPages / totalPages * 100)
</script>

<div class="container_100 progressbar">
    <div class="container_100 bg_light_grey">
        <div class="bg_main" style={"width:" + progress + "%;"}></div>
    </div>
    <span class="font_small">{conf.book.progress_one} {progressPages} {conf.book.progress_two} {totalPages}</span>
</div>