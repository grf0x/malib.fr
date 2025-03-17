<script>
    let fsContainer;
    let fullScreenOn = false;
    const blank = ()=>{};
    export const fullScreenSupport = !!(document.fullscreenEnabled || document.webkitFullscreenEnabled || document.mozFullScreenEnabled || document.msFullscreenEnabled || false);
    const exitFullscreen = (document.exitFullscreen || document.mozCancelFullScreen || document.webkitExitFullscreen || document.msExitFullscreen || blank).bind(document);
    const requestFullscreen = () => {
        const requestFS = (fsContainer.requestFullscreen || fsContainer.mozRequestFullScreen || fsContainer.webkitRequestFullscreen || fsContainer.msRequestFullscreen || blank).bind(fsContainer);
        requestFS();
    };

    export const funcs = {
        request(){
            if(fullScreenOn){
                exitFullscreen();
                fullScreenOn = false;
            }
            else{
                requestFullscreen();
                fullScreenOn = true;
            }
        },
        exit(){
            exitFullscreen();
            fullScreenOn = false;
        }
    };

</script>

<div bind:this={fsContainer}>
    <slot/>
</div>