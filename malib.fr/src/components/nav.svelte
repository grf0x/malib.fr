<script>
    import * as conf from "../app.json";
    import { logout, api, goTo, currentRoute, bookCredit, clickOutside, unreadNotifications, isSub, pickFirstBook, nextCreditDate } from "../app.js";
    import Link from "./link.svelte";
    import Button from "./button.svelte";
    const date = { month: "long", day: "numeric" };
    const notifDateFirst = { month: "numeric", day: "numeric"};
    const notifDateSecond = { year:"numeric"};
    let visibility = { "settings": true, "notifications": false, "books": false };
    let notifications = [];

    function hideAll(){
        for(let e in visibility) {
            visibility[e] = false;
        }
    }

    async function clickIcon(element){
        for(let e in visibility) {
            if(e === element && !visibility[e]){
                if(e === "notifications")
                    await getNotifications();
                visibility[e] = true;
            }
            else
                visibility[e] = false;
        }
    }

    async function getNotifications(){
        let r = await api("/notifications", "get", {}, {});
        if(r.status == 200){
            notifications = r.data;   
            $unreadNotifications = 0;     
        }
    }

    $:$currentRoute, hideAll()
</script>

<nav use:clickOutside={()=>{hideAll()}}>

{#if $unreadNotifications > 0 && $pickFirstBook}
<div class="absolute md:top-[1.2rem] top-[0.9rem] md:right-[3.4rem] right-[3.45rem] md:text-[0.55rem] text-[0.6rem] font-mono flex bg-gradient-to-r from-custom-red-dark to-custom-red-light rounded-full md:w-[1.1rem] md:h-[1.1rem] w-5 h-5 justify-center items-center cursor-default">{$unreadNotifications > 99 ? "99+" : $unreadNotifications}</div>
{/if}

{#if $bookCredit > 0 && $pickFirstBook && $isSub}
<div class="absolute md:top-[1.2rem] top-[0.9rem] md:right-[5.6rem] right-[6.35rem] md:text-[0.55rem] text-[0.6rem] font-mono flex bg-gradient-to-r from-custom-red-dark to-custom-red-light rounded-full md:w-[1.1rem] md:h-[1.1rem] w-5 h-5 justify-center items-center cursor-default">{$bookCredit}</div>
{/if}

<div class="flex">
    {#if $isSub && $pickFirstBook}
    <img class="md:w-6 md:h-6 md:ml-3 w-8 h-8 ml-4 cursor-pointer" src="imgs/book.png" alt="book" on:click={()=>{clickIcon("books")}}/>
    {/if}
    {#if $pickFirstBook}
    <img class="md:w-6 md:h-6 md:ml-3 w-8 h-8 ml-4 cursor-pointer" src="imgs/bell.png" alt="bell" on:click={()=>{clickIcon("notifications");}}/>
    {/if}
    <img class="md:w-6 md:h-6 md:ml-3 w-8 h-8 ml-4 cursor-pointer" src="imgs/settings.png" alt="settings" on:click={()=>{clickIcon("settings")}}/>
</div>

{#if visibility.books}
<div class="triangle absolute md:top-[3.6rem] top-[3.8rem] md:right-[6.1rem] right-[7.05rem]"></div>
<div class="absolute m md:top-[4.4rem] top-[4.6rem] md:right-[5.5rem] right-[2.5%] flex px-4 md:pt-4 md:pb-5 pt-6 pb-8 flex-col md:w-72 rounded-lg w-[95%] bg-white text-black z-50 shadow-md shadow-neutral-700">
    {#if $bookCredit > 0}
    <span class="text-center">{$bookCredit + " " + ($bookCredit === 1 ? conf.book_credit : conf.book_credit_plural)}</span>
    <Button cls="mt-2" to={conf.pages.new_book.route}>{conf.button.choose_book}</Button>
    {:else}
    <div class="w-full text-center">{conf.next_book_date + " " + $nextCreditDate.toLocaleDateString(conf.date_format, date)}</div>
    {/if}
</div>
{/if}


{#if notifications.length && visibility.notifications}
<div class="triangle absolute md:top-[3.6rem] top-[3.8rem] md:right-[3.8rem] right-[4.05rem]"></div>
<div class="absolute md:top-[4.4rem] top-[4.6rem] md:right-[3.25rem] right-[2.5%] flex flex-col md:w-[25rem] max-h-96 rounded-lg w-[95%] bg-white text-black z-50 shadow-md shadow-neutral-700 overflow-scroll no-scrollbar">
    {#each notifications as n}
    <div class="flex w-full p-4 justify-center items-center">
        <div class="w-16 h-16 flex-shrink-0 p-2 items-center justify-center rounded-lg bg-gradient-to-r from-custom-red-dark to-custom-red-light">
            <img class="w-full h-full" src={conf.notification[n.type].img} alt="img">
        </div>
        <div class="flex flex-grow text-sm items-center justify-center">
            <h3 class="flex flex-grow px-4">{conf.notification[n.type].msg}</h3>
            <span class="flex flex-col justify-center items-center text-center text-xs w-16 h-16 rounded-lg bg-neutral-100 flex-shrink-0">{new Date(n.date).toLocaleDateString(conf.date_format, notifDateFirst)}<br/>{new Date(n.date).toLocaleDateString(conf.date_format, notifDateSecond)}</span>
        </div>
    </div>
    <hr class="border-neutral-300">
    {/each}
</div>
{/if}

{#if visibility.settings}
<div class="triangle absolute md:top-[3.6rem] top-[3.8rem] md:right-[1.60rem] right-[1.05rem]"></div>
<div class="absolute md:top-[4.4rem] top-[4.6rem] flex flex-col md:w-52 rounded-lg w-[95%] md:right-4 right-[2.5%] bg-white text-black z-50 shadow-md shadow-neutral-700">
    <Link to={conf.pages.account.route} cls="md:py-4 py-8 text-center hover:underline">{conf.pages.account.title}</Link>
    <hr class="border-neutral-300">
    <Link to={conf.pages.referral.route} cls="md:py-4 py-8  text-center hover:underline">{conf.pages.referral.title}</Link>
    <hr class="border-neutral-300">
    <span on:click={()=>{logout(); goTo(conf.pages.welcome.route)}} class="md:py-4 py-8  text-center hover:underline cursor-pointer">{conf.logout}</span>
</div>
{/if}

</nav>

<style>
.triangle{
    display : inline-block;
    height : 0;
    width : 0;
    border-right : 11px solid transparent;
    border-bottom : 16px solid white;
    border-left : 11px solid transparent;
   }
</style>