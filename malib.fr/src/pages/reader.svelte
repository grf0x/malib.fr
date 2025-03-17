<script>
    import * as conf from "../app.json";
    import Logo from "../components/logo.svelte";
    import Spinner from "../components/spinner.svelte";
    import NavTheme from "../components/navTheme.svelte";
    import NavFontSize from "../components/navFontSize.svelte";
    import NavFontFamily from "../components/navFontFamily.svelte";
    import NavChapters from "../components/navChapters.svelte";
    import ReaderProgressBar from "../components/readerProgressBar.svelte";
    import Fullscreen from "../components/fullscreen.svelte";
    import ePub from "epubjs/dist/epub.min.js";
    import { onMount, onDestroy } from "svelte";
    import { goTo, params, clickOutside, settingLibrarySorting, settingReaderFont, settingReaderZoom, settingReaderTheme, cacheLibrary, api } from "../app.js";
    let savedChapterProgress;
    let savedHref;
    let bookUrl;
    let bookId;
    let timeOutSave;
    let timeIntervalSave = 500;
    let isPageLoading = true;
    let showProgressSpinner = true;
    let settingsMenuVisible = false;
    let chaptersMenuVisible = false;
    let notesMenuVisible = false;
    let uiReady = false;
    let fullScreen;
    let fullScreenSupport;
    let fontSize = 130;
    let fontFamily = "FUTURA";
    let themeName = "DGREY";
    let theme = conf.themes.DGREY;
    let disableSelect = false;
    let bookTitle = "-";
    let chapterTitle = "-";
    let bookProgress = 0;
    let chapterProgress = 0;
    let tocList = [];
    let currentCfi = 0;
    let currentHref = 0;
    let book;
    let reader;
    
    function generateTheme(t){
        return {
            "@font-face":{
                "font-family": fontFamily, 
                "src": "url('/fonts/" + fontFamily.toLowerCase() + ".otf')"
            },
            "body": {
                "font-size" : fontSize + "% !important",
                "font-family": fontFamily + " !important",
                "background": t.background + " !important",
                "text-align": "justify !important",
                "color": t.color + " !important",
            },
            "p":{
                "padding": "0 !important",
                "margin": "0 !important",
                "line-height": "150% !important",
                "padding-bottom": "1rem !important",
            },
            "a": {
                "color": "inherit !important",
                "text-decoration": "none !important",
                "-webkit-text-fill-color": "inherit !important"
            },
            "a:link": {
                "color": t.link + " !important",
                "text-decoration": "none !important",
                "-webkit-text-fill-color": t.link + " !important"
            },
            "a:link:hover": {
                "opacity": "0.5 !important"
            },
            "img": {
                "max-width": "100% !important"
            }
        }  
    }

    function generateTocList(){
        let list = [];
        let browseTocItems = function(toc, level = 0){
		    for(const chapter of toc){
                list.push({"label":chapter.label, "href":chapter.href, "level":level});
                if(chapter.subitems && chapter.subitems.length > 0)
                    browseTocItems(chapter.subitems, level + 1);
            }
		}
        browseTocItems(book.navigation.toc);
        return list;
    }

    function updateLocation(location, save=true){
        if(book && reader){
            currentCfi = location.start.cfi;
            currentHref = location.start.href;
            chapterTitle = book.navigation.get(currentHref).label;
            bookProgress = location.end.percentage * 100;
            chapterProgress = location.end.displayed.page / location.end.displayed.total * 100;
            if(!isPageLoading && uiReady){
                savedHref = currentHref;
                savedChapterProgress = chapterProgress;
                if(save)
                    saveProgress();
            }
        }
    }

    function handleKeyDown(event){
        if(event.key === "ArrowLeft" && reader)
            reader.prev();
        else if(event.key === "ArrowRight"&& reader)
            reader.next();
    }

    async function saveProgress(){ 
        clearTimeout(timeOutSave);
        timeOutSave = setTimeout(()=> {
            api("/save-progress", "post", {}, {book_id:bookId, chapter:currentHref, progress_chapter:chapterProgress.toFixed(4), progress_book:bookProgress.toFixed(4)});
        }
        ,3000);
    }

    async function loadPage(href, percentageChapter){
        if(reader){
            isPageLoading = true;
            try{  
                await reader.display(href);
                await reader.next();
                await reader.prev();   
                if(Object.keys(reader.currentLocation()).length === 0){
                    await sleep(500);
                    await render();
                    return;
                }
                let loc = reader.currentLocation();
                let target = Math.round((loc.start.displayed.total / 100) * percentageChapter);
                let current = loc.end.displayed.page;
                let step = loc.end.displayed.page - loc.start.displayed.page + 1;
                while(current < target){
                    await reader.next();
                    current += step;
                }
            }catch{
                await reader.display();
            }
            isPageLoading = false;
        }
    }

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async function render(){
        if(book){
            if(reader)
                reader.destroy();
            reader = book.renderTo("viewer", {method:"continuous", width:"100%", height:"100%"});  
            reader.themes.default(generateTheme(conf.themes[themeName])); 
            await loadPage(savedHref, savedChapterProgress);
            reader.on('relocated', function(location){updateLocation(location)});
            reader.on('selected', function(cfirange, data, contents){alert(currentCfi + " " + cfirange)});
            reader.on('keydown', handleKeyDown);
        }
    }

    async function updateSettings(){
        if(uiReady){
            $settingReaderZoom = fontSize;
            $settingReaderFont = fontFamily;
            $settingReaderTheme = themeName;
            let settings = {"library_sorting":$settingLibrarySorting, "reader_theme":$settingReaderTheme, "reader_zoom":$settingReaderZoom, "reader_font":$settingReaderFont};
            api("/change-settings", "post", {}, settings);
        }
        render();
    }

    async function init_data(){
        bookId = $params.id;
        bookUrl = conf.book_url + bookId + ".epub";
        let r = await api("/progress", "get", {book_id:bookId}, {});
        if(r.status == 200){
            savedHref = r.data.chapter;
            savedChapterProgress = r.data.progress_chapter;
        }else
            goTo(conf.pages.new_book.route + "?id=" + bookId);
        fontSize = $settingReaderZoom;
        fontFamily = $settingReaderFont;
        themeName = $settingReaderTheme;
        theme = conf.themes[$settingReaderTheme];
    }

    onMount(async()=>{
        if(!$params.id)
            goTo(conf.pages.library.route);
        await init_data();
        book = ePub(bookUrl, { openAs: "epub" }); 
        await book.ready;
        bookTitle = book.package.metadata.title;
        tocList = generateTocList();
        uiReady = true;
        $cacheLibrary = null;
        await book.locations.generate(300);
        await render();
        showProgressSpinner = false;  
        if(reader)
            updateLocation(reader.currentLocation(), false);
    });

    $:fontSize, updateSettings();
    $:themeName, updateSettings();
    $:fontFamily, updateSettings();
</script>
<svelte:window on:keydown={handleKeyDown} on:resize={()=>{render()}}/>
<Fullscreen bind:fullScreenSupport={fullScreenSupport} bind:funcs={fullScreen}>
{#if settingsMenuVisible || chaptersMenuVisible || notesMenuVisible}
<div class="absolute h-full w-full z-10"></div>
{/if}

{#if isPageLoading}
<div style="background-color:{theme.background};" class="absolute h-full w-full flex justify-center items-center z-10">
    <Spinner color={theme.color} size="big"/>
</div>
{/if}

<div style="background-color:{theme.background}; color:{theme.color};" class="flex flex-col h-screen w-full" class:select-none={disableSelect}>
    <div style="background-color:{theme.background}; color:{theme.color};" class="w-full py-3 flex flex-row align-baseline items-center justify-between md:px-6 px-3 select-none z-20">
        <Logo on:click={()=>{fullScreen.exit(); goTo(conf.pages.library.route)}} color={theme.color}/>
        <div use:clickOutside={()=>{settingsMenuVisible = false; chaptersMenuVisible = false; notesMenuVisible = false;}} class="flex text-sm justify-center items-center">
            {#if fullScreenSupport}
            <div on:click={()=>{fullScreen.request(); chaptersMenuVisible = false; settingsMenuVisible = false; notesMenuVisible = false;}} style="background:{theme.color}" class="flex justify-center items-center h-8 w-8 mr-1 rounded-full cursor-pointer z-50"><svg fill={theme.background} class="w-4 h-4" viewBox="0 0 512 512" style="enable-background:new 0 0 512 512;" version="1.1" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><g id="Layer_1"/><g id="Layer_2"><g><path class="st0" d="M468.19,452.12V332.16c0-8.84-7.16-16-16-16s-16,7.16-16,16v81.6c-22.57-22.42-56.18-55.82-89.22-88.75    V186.99c33.05-32.92,66.65-66.32,89.22-88.74v81.59c0,8.84,7.16,16,16,16s16-7.16,16-16V59.88c0-0.01,0-0.01,0-0.02v-0.05    c0-0.12-0.02-0.23-0.02-0.35c-0.01-0.4-0.02-0.81-0.06-1.21c-0.02-0.23-0.06-0.45-0.1-0.68c-0.04-0.29-0.08-0.58-0.13-0.87    c-0.05-0.25-0.12-0.5-0.18-0.75c-0.06-0.26-0.12-0.51-0.2-0.77c-0.07-0.25-0.17-0.49-0.25-0.73c-0.09-0.25-0.17-0.5-0.27-0.75    c-0.1-0.23-0.21-0.45-0.31-0.68c-0.12-0.25-0.23-0.5-0.36-0.74c-0.12-0.22-0.25-0.42-0.37-0.64c-0.14-0.24-0.28-0.48-0.43-0.71    c-0.15-0.23-0.32-0.44-0.48-0.66c-0.15-0.2-0.29-0.4-0.45-0.6c-0.23-0.29-0.48-0.55-0.74-0.82c-0.1-0.11-0.19-0.23-0.3-0.33    c-0.01-0.01-0.02-0.01-0.02-0.02c-0.37-0.37-0.76-0.73-1.17-1.06c-0.16-0.13-0.34-0.25-0.5-0.38c-0.25-0.19-0.49-0.38-0.75-0.56    c-0.22-0.15-0.45-0.28-0.68-0.42c-0.22-0.13-0.43-0.27-0.66-0.39c-0.23-0.12-0.46-0.22-0.69-0.33c-0.24-0.12-0.48-0.24-0.73-0.34    c-0.21-0.09-0.43-0.16-0.65-0.24c-0.28-0.1-0.55-0.21-0.83-0.29c-0.2-0.06-0.41-0.1-0.61-0.16c-0.3-0.08-0.6-0.16-0.91-0.23    c-0.22-0.04-0.45-0.07-0.67-0.1c-0.29-0.05-0.58-0.1-0.88-0.13c-0.52-0.05-1.04-0.08-1.56-0.08c-0.01,0-0.03,0-0.04,0H332.16    c-8.84,0-16,7.16-16,16s7.16,16,16,16h81.21c-22.51,22.36-55.86,55.5-88.69,88.21H185.97c-32.59-32.72-65.54-65.87-87.73-88.21    h81.6c8.84,0,16-7.16,16-16s-7.16-16-16-16H59.81c-0.16,0-0.32,0.02-0.48,0.02c-0.35,0.01-0.71,0.02-1.06,0.05    c-0.26,0.02-0.5,0.07-0.75,0.11c-0.26,0.04-0.53,0.07-0.79,0.12c-0.27,0.05-0.54,0.13-0.8,0.19c-0.24,0.06-0.48,0.11-0.72,0.18    c-0.26,0.08-0.52,0.18-0.77,0.27c-0.24,0.08-0.47,0.16-0.71,0.26c-0.24,0.1-0.47,0.22-0.71,0.33c-0.24,0.11-0.48,0.22-0.71,0.34    c-0.23,0.12-0.45,0.26-0.67,0.39c-0.23,0.14-0.46,0.26-0.68,0.41c-0.24,0.16-0.46,0.33-0.69,0.5c-0.19,0.14-0.38,0.27-0.57,0.43    c-0.3,0.25-0.58,0.51-0.87,0.78c-0.09,0.09-0.2,0.17-0.29,0.26c-0.01,0.01-0.01,0.01-0.02,0.02c-0.37,0.37-0.73,0.76-1.07,1.17    c-0.13,0.16-0.24,0.33-0.37,0.49c-0.19,0.25-0.39,0.5-0.56,0.76c-0.15,0.23-0.29,0.47-0.43,0.7c-0.13,0.21-0.26,0.42-0.38,0.64    c-0.13,0.24-0.24,0.49-0.35,0.73c-0.11,0.23-0.22,0.45-0.32,0.69c-0.1,0.23-0.17,0.47-0.26,0.71c-0.09,0.25-0.19,0.51-0.27,0.77    c-0.07,0.23-0.12,0.47-0.18,0.71c-0.07,0.27-0.15,0.53-0.2,0.81c-0.06,0.3-0.1,0.6-0.14,0.9c-0.03,0.22-0.07,0.43-0.1,0.65    c-0.05,0.52-0.08,1.05-0.08,1.58c0,0.01,0,0.02,0,0.03v120.03c0,8.84,7.16,16,16,16s16-7.16,16-16V98.63    c22.36,22.51,55.51,55.86,88.21,88.69v137.36c-32.71,32.83-65.85,66.18-88.21,88.69v-81.21c0-8.84-7.16-16-16-16s-16,7.16-16,16    v120.03c0,0.01,0,0.02,0,0.03c0,0.53,0.03,1.05,0.08,1.58c0.02,0.21,0.06,0.42,0.09,0.62c0.04,0.31,0.08,0.62,0.14,0.92    c0.05,0.27,0.13,0.53,0.2,0.79c0.06,0.24,0.11,0.49,0.19,0.73c0.08,0.26,0.18,0.5,0.27,0.75c0.09,0.24,0.17,0.49,0.27,0.73    c0.1,0.23,0.21,0.45,0.31,0.67c0.12,0.25,0.23,0.5,0.36,0.75c0.11,0.21,0.24,0.41,0.36,0.61c0.15,0.25,0.28,0.49,0.44,0.73    c0.16,0.24,0.34,0.47,0.52,0.7c0.14,0.19,0.27,0.38,0.42,0.56c0.33,0.41,0.69,0.79,1.06,1.17c0.01,0.01,0.01,0.02,0.02,0.02    c0.11,0.11,0.23,0.2,0.34,0.31c0.26,0.25,0.53,0.5,0.81,0.73c0.2,0.16,0.4,0.3,0.61,0.45c0.22,0.16,0.43,0.32,0.65,0.47    c0.23,0.15,0.47,0.29,0.71,0.43c0.21,0.12,0.41,0.25,0.63,0.37c0.24,0.13,0.49,0.24,0.74,0.36c0.22,0.1,0.44,0.22,0.67,0.31    c0.24,0.1,0.49,0.18,0.74,0.27c0.24,0.09,0.48,0.18,0.73,0.25c0.25,0.08,0.5,0.13,0.76,0.19c0.25,0.06,0.5,0.13,0.76,0.18    c0.29,0.06,0.58,0.09,0.87,0.13c0.22,0.03,0.45,0.07,0.67,0.1c0.52,0.05,1.05,0.08,1.58,0.08h0h0h120.03c8.84,0,16-7.16,16-16    s-7.16-16-16-16H98.24c22.42-22.57,55.82-56.18,88.74-89.22h136.68c33.16,33.04,66.96,66.63,89.7,89.22h-81.21    c-8.84,0-16,7.16-16,16s7.16,16,16,16h120.03c0.53,0,1.06-0.03,1.58-0.08c0.24-0.02,0.48-0.07,0.72-0.1    c0.28-0.04,0.55-0.07,0.83-0.13c0.27-0.05,0.54-0.13,0.81-0.2c0.24-0.06,0.48-0.11,0.71-0.18c0.26-0.08,0.51-0.18,0.77-0.27    c0.24-0.09,0.48-0.16,0.71-0.26c0.23-0.1,0.46-0.21,0.69-0.32c0.25-0.12,0.5-0.23,0.74-0.35c0.21-0.11,0.42-0.25,0.62-0.37    c0.24-0.14,0.49-0.28,0.72-0.44c0.24-0.16,0.46-0.34,0.69-0.51c0.19-0.14,0.39-0.27,0.57-0.43c0.41-0.33,0.79-0.69,1.17-1.06    c0.01-0.01,0.02-0.02,0.03-0.02c0.12-0.12,0.22-0.25,0.33-0.37c0.24-0.26,0.48-0.51,0.7-0.78c0.16-0.2,0.31-0.41,0.46-0.62    c0.16-0.21,0.32-0.42,0.47-0.64c0.16-0.23,0.29-0.48,0.44-0.72c0.12-0.21,0.25-0.41,0.37-0.63c0.13-0.25,0.24-0.5,0.36-0.75    c0.1-0.22,0.21-0.44,0.31-0.67c0.1-0.25,0.19-0.5,0.28-0.75c0.09-0.24,0.18-0.48,0.25-0.73c0.08-0.25,0.13-0.51,0.2-0.77    c0.06-0.25,0.13-0.5,0.18-0.75c0.06-0.29,0.09-0.58,0.13-0.87c0.03-0.23,0.07-0.45,0.1-0.68c0.04-0.4,0.05-0.8,0.06-1.2    c0-0.12,0.02-0.24,0.02-0.36v-0.05C468.19,452.13,468.19,452.13,468.19,452.12z M196.02,196.02h118.95v118.95H196.02V196.02z"/></g></g></svg></div>
            {/if}
            <!--<div on:click={()=>{notesMenuVisible = !notesMenuVisible; chaptersMenuVisible = false; settingsMenuVisible = false;}} style="background:{theme.color}" class="flex justify-center items-center h-8 w-8 rounded-full cursor-pointer mr-1 z-50"><svg fill={theme.background} class="w-[0.95rem] h-[0.95rem] ml-[0.1rem] mb-[0.05rem]" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg"><path d="M799.344 960.288h-736v-800h449.6l64.704-62.336-1.664-1.664H63.344c-35.344 0-64 28.656-64 64v800c0 35.344 28.656 64 64 64h736c35.344 0 64-28.656 64-64V491.632l-64 61.088v407.568zM974.224 41.44C945.344 13.76 913.473-.273 879.473-.273c-53.216 0-92.032 34.368-102.592 44.897-14.976 14.784-439.168 438.353-439.168 438.353-3.328 3.391-5.76 7.535-7.008 12.143-11.488 42.448-69.072 230.992-69.648 232.864-2.976 9.664-.32 20.193 6.8 27.217a26.641 26.641 0 0 0 18.913 7.84c2.752 0 5.52-.4 8.239-1.248 1.952-.656 196.496-63.569 228.512-73.12 4.224-1.248 8.048-3.536 11.216-6.624 20.208-19.936 410.112-403.792 441.664-436.384 32.624-33.664 48.847-68.657 48.223-104.097-.591-35.008-17.616-68.704-50.4-100.128zm-43.791 159.679c-17.808 18.368-157.249 156.16-414.449 409.536l-19.68 19.408c-29.488 9.12-100.097 31.808-153.473 49.024 17.184-56.752 37.808-125.312 47.008-157.743C444.8 466.464 808.223 103.6 822.03 89.968c2.689-2.689 27.217-26.257 57.44-26.257 17.153 0 33.681 7.824 50.465 23.92 20.065 19.248 30.4 37.744 30.689 55.024.32 17.792-9.84 37.456-30.191 58.464z"/></svg></div>-->
            <div on:click={()=>{settingsMenuVisible = !settingsMenuVisible; chaptersMenuVisible = false; notesMenuVisible = false;}} style="background:{theme.color}" class="flex justify-center items-center h-8 w-8 mr-1 rounded-full cursor-pointer z-50"><svg fill={theme.background} class="w-4 h-4" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"	 viewBox="0 0 480.3 480.3" style="enable-background:new 0 0 480.3 480.3;" xml:space="preserve"><g>	<g>		<path d="M254.15,234.1V13.5c0-7.5-6-13.5-13.5-13.5s-13.5,6-13.5,13.5v220.6c-31.3,6.3-55,34-55,67.2s23.7,60.9,55,67.2v98.2			c0,7.5,6,13.5,13.5,13.5s13.5-6,13.5-13.5v-98.2c31.3-6.3,55-34,55-67.2C309.15,268.2,285.55,240.4,254.15,234.1z M240.65,342.8			c-22.9,0-41.5-18.6-41.5-41.5s18.6-41.5,41.5-41.5s41.5,18.6,41.5,41.5S263.55,342.8,240.65,342.8z"/>		<path d="M88.85,120.9V13.5c0-7.5-6-13.5-13.5-13.5s-13.5,6-13.5,13.5v107.4c-31.3,6.3-55,34-55,67.2s23.7,60.9,55,67.2v211.4			c0,7.5,6,13.5,13.5,13.5s13.5-6,13.5-13.5V255.2c31.3-6.3,55-34,55-67.2S120.15,127.2,88.85,120.9z M75.35,229.6			c-22.9,0-41.5-18.6-41.5-41.5s18.6-41.5,41.5-41.5s41.5,18.6,41.5,41.5S98.15,229.6,75.35,229.6z"/>		<path d="M418.45,120.9V13.5c0-7.5-6-13.5-13.5-13.5s-13.5,6-13.5,13.5v107.4c-31.3,6.3-55,34-55,67.2s23.7,60.9,55,67.2v211.5			c0,7.5,6,13.5,13.5,13.5s13.5-6,13.5-13.5V255.2c31.3-6.3,55-34,55-67.2S449.85,127.2,418.45,120.9z M404.95,229.6			c-22.9,0-41.5-18.6-41.5-41.5s18.6-41.5,41.5-41.5s41.5,18.6,41.5,41.5S427.85,229.6,404.95,229.6z"/>	</g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g></svg></div>
            <div on:click={()=>{chaptersMenuVisible = !chaptersMenuVisible; settingsMenuVisible = false; notesMenuVisible = false;}} style="background:{theme.color}" class="flex justify-center items-center h-8 w-8 rounded-full cursor-pointer z-50"><svg fill={theme.background} class="w-[1.1rem] h-[1.1rem]" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg" ><path d="M64 96L112 96 112 144 64 144 64 96ZM160 96L448 96 448 144 160 144 160 96ZM64 232L112 232 112 280 64 280 64 232ZM160 232L448 232 448 280 160 280 160 232ZM64 368L112 368 112 416 64 416 64 368ZM160 368L448 368 448 416 160 416 160 368Z" /></svg>
            </div>
            {#if notesMenuVisible}
            <div style="border-bottom: 16px solid {theme.color}" class="triangle absolute md:top-[3.6rem] top-[3.8rem] md:right-[6.30rem] right-[5.55rem] z-50"></div>
            <div style="background-color: {theme.color}; color: {theme.color};" class="absolute md:top-[4.4rem] top-[4.6rem] flex flex-col md:w-60 rounded-lg w-[95%] md:right-[5.80rem] right-[2.5%] z-50">
            </div>
            {/if}
            {#if settingsMenuVisible}
            <div style="border-bottom: 16px solid {theme.color}" class="triangle absolute md:top-[3.6rem] top-[3.8rem] md:right-[4.05rem] right-[3.30rem] z-50"></div>
            <div style="background-color: {theme.color}; color: {theme.color};" class="absolute md:top-[4.4rem] top-[4.6rem] flex flex-col md:w-60 rounded-lg w-[95%] md:right-[3.55rem] right-[2.5%] z-50">
                <NavFontSize {theme} bind:size={fontSize}/>
                <hr style="border-color:{theme.background}">
                <NavTheme bind:theme={theme} bind:themeName={themeName}/>
                <hr style="border-color:{theme.background}">
                <NavFontFamily {theme} bind:font={fontFamily}/>
            </div>
            {/if}
            {#if chaptersMenuVisible}
            <div style="border-bottom: 16px solid {theme.color}" class="triangle absolute md:top-[3.6rem] top-[3.8rem]  md:right-[1.80rem] right-[1.05rem] z-50"></div>
            <div style="background-color: {theme.color}; color: {theme.color};" class="absolute md:top-[4.4rem] top-[4.6rem] flex flex-col md:w-96 rounded-lg w-[95%] md:right-[1.30rem] right-[2.5%] z-50">
                <NavChapters {theme} {tocList} {reader} {currentHref}/>
            </div>
            {/if}
        </div>
    </div>

    <div on:click={()=>{reader.prev()}} on:mouseenter={()=>{disableSelect = true}} on:mouseleave={()=>{disableSelect = false}} class="absolute cursor-pointer duration-300 left-0 flex h-full w-16 opacity-0 items-center justify-center z-10 hover:opacity-100">
        <div style="background:{theme.color}" class="absolute md:visible invisible flex justify-center items-center h-8 w-8 rounded-full cursor-pointer z-50"><svg fill={theme.background} class="w-7 h-7" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path clip-rule="evenodd" d="M14.5303 18.5303C14.2374 18.8232 13.7626 18.8232 13.4697 18.5303L7.46967 12.5303C7.17678 12.2374 7.17678 11.7626 7.46967 11.4697L13.4697 5.46967C13.7626 5.17678 14.2374 5.17678 14.5303 5.46967C14.8232 5.76256 14.8232 6.23744 14.5303 6.53033L9.06066 12L14.5303 17.4697C14.8232 17.7626 14.8232 18.2374 14.5303 18.5303Z"/></svg></div>
    </div>
    <div id="viewer" class="h-full w-full md:px-6 px-4 pb-6 z-0"></div>
    <div on:click={()=>{reader.next()}} on:mouseenter={()=>{disableSelect = true}} on:mouseleave={()=>{disableSelect = false}} class="absolute cursor-pointer duration-300 right-0 flex h-full w-16 opacity-0 items-center justify-center z-10 hover:opacity-100">
        <div style="background:{theme.color}" class="absolute md:visible invisible flex justify-center items-center h-8 w-8 rounded-full cursor-pointer z-50"><svg fill={theme.background} class="w-7 h-7" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path clip-rule="evenodd" d="M9.46967 5.46967C9.76256 5.17678 10.2374 5.17678 10.5303 5.46967L16.5303 11.4697C16.8232 11.7626 16.8232 12.2374 16.5303 12.5303L10.5303 18.5303C10.2374 18.8232 9.76256 18.8232 9.46967 18.5303C9.17678 18.2374 9.17678 17.7626 9.46967 17.4697L14.9393 12L9.46967 6.53033C9.17678 6.23744 9.17678 5.76256 9.46967 5.46967Z"/></svg></div>
    </div>
    <ReaderProgressBar {showProgressSpinner} {bookTitle} {chapterTitle} {theme} {bookProgress} {chapterProgress}/>
</div>
</Fullscreen>
<style>
.triangle{
    display : inline-block;
    height : 0;
    width : 0;
    border-right : 11px solid transparent;
    border-left : 11px solid transparent;
   }
</style>