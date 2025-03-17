<script>
    import Header from "../components/header.svelte";
    import Footer from "../components/footer.svelte";
    import Button from "../components/button.svelte";
    import Error from "../components/error.svelte";
    import InputText from "../components/inputText.svelte";
    import Link from "../components/link.svelte";
    import ButtonChoice from "../components/buttonChoice.svelte";
    import * as conf from "../app.json";
    import { api, goTo, isSub, email, emailPrefNewBook, emailPrefRefSomeone, emailPrefSubWillExpire, emailPrefPromo, updateAuthInfo, isDiscount, subSince, isSubCanceled, subCurrentPeriodEnd } from "../app.js";
    let disableButtonsEmailPref = false;
    let buttonSpinnerStopCancelation = false;
    const dateDay = { year: "numeric", month: "long", day: "numeric"};
    const dateMonth = { year: "numeric", month: "long" };

    async function changePrefEmail(name, actual_state){
        disableButtonsEmailPref = true
        let pref = {"new_book":$emailPrefNewBook, "ref_someone":$emailPrefRefSomeone, "sub_will_expire":$emailPrefSubWillExpire, "promo":$emailPrefPromo};
        pref[name] = !actual_state;
        let r = await api("/change-email-preferences", "post", {}, pref);  
        if(r.status == 200){
            if(name === "new_book")
                $emailPrefNewBook = !$emailPrefNewBook;
            else if(name === "ref_someone")
                $emailPrefRefSomeone = !$emailPrefRefSomeone;
            else if(name === "sub_will_expire")
                $emailPrefSubWillExpire = !$emailPrefSubWillExpire;
            else if(name === "promo")
                $emailPrefPromo = !$emailPrefPromo;
        }   
        disableButtonsEmailPref = false;
    }

    async function stopSubscriptionCancelation(){
        buttonSpinnerStopCancelation = true;
        let r = await api("/cancel-subscription", "post", {}, {state:false});  
        if(r.status == 200)
            $isSubCanceled = false;
        buttonSpinnerStopCancelation = false;
    }
</script>

<div class="min-h-screen flex flex-col">
    <Header></Header>
    <div class="flex flex-grow flex-col justify-center items-center self-center text-center md:px-6 px-3 w-full pt-2 pb-16">
        <div class="max-w-5xl w-full">
            <div class="flex flex-col md:p-8 p-6 pb-8 pt-8 md:pb-10 mb-8 rounded-lg bg-neutral-800">
                <h2 class="font-futurar md:text-2xl text-xl mb-4">{conf.account.credentials}</h2>
                <div class="flex md:flex-row flex-col w-full md:space-x-4 md:space-y-0 space-y-4 mb-4 justify-center">
                    <div class="w-full p-4 border-black border rounded-lg bg-white text-black"><h4>{$email}</h4></div>
                    <div class="w-full p-4 border-black border rounded-lg bg-white text-black"><h4>{conf.account.password}</h4></div>
                </div>
                <div class="flex md:flex-row flex-col w-full md:space-x-4 md:space-y-0 space-y-4 justify-center">
                    <Button to={conf.pages.change_email.route} size="medium" cls="w-full">{conf.account.change_email}</Button>
                    <Button to={conf.pages.change_password.route} size="medium" cls="w-full">{conf.account.change_password}</Button>
                </div>
            </div>
            <div class="flex flex-col md:p-8 p-6 pb-8 pt-8 md:pb-10 mb-8 rounded-lg bg-neutral-800">
                <h2 class="font-futurar md:text-2xl text-xl mb-4">{conf.account.membership}</h2>
            {#if $isSub}
                {#if $isSubCanceled}
                <div class="flex md:flex-row flex-col w-full md:space-x-4 md:space-y-0 space-y-4 mb-4 justify-center">
                    <div class="w-full p-4 pt-5 border-black border rounded-lg bg-white text-black"><h4>{conf.account.member_since} {$subSince.toLocaleDateString(conf.date_format, dateMonth)}</h4></div>
                    <div class="w-full p-4 font-extrabold border-custom-red text-custom-red border-4 rounded-lg"><h4>{conf.account.cancel_subscription_on} {$subCurrentPeriodEnd.toLocaleDateString(conf.date_format, dateDay)}</h4></div>
                </div>
                <div class="flex md:flex-row flex-col w-full md:space-x-4 md:space-y-0 space-y-4 justify-center">
                    <Button bind:showSpinner={buttonSpinnerStopCancelation} on:click={stopSubscriptionCancelation} size="medium" cls="w-full max-w-lg">{conf.account.cancel_unsubscribe}</Button>
                </div>
                {:else}
                <div class="flex md:flex-row flex-col w-full md:space-x-4 md:space-y-0 space-y-4 mb-4 justify-center">
                    <div class="w-full p-4 border-black border rounded-lg bg-white text-black"><h4>{conf.account.member_since} {$subSince.toLocaleDateString(conf.date_format, dateMonth)}</h4></div>
                    <div class="w-full p-4 border-black border rounded-lg bg-white text-black"><h4>{conf.account.next_bill_one} {$isDiscount ? conf.referrer_price : conf.not_a_referrer_price} {conf.account.next_bill_two} {$subCurrentPeriodEnd.toLocaleDateString(conf.date_format, dateDay)}</h4></div>
                </div>
                <div class="flex md:flex-row flex-col w-full md:space-x-4 md:space-y-0 space-y-4 justify-center">
                    <Button to={conf.pages.unsubscribe.route} size="medium" cls="w-full max-w-lg">{conf.account.unsubscribe}</Button>
                </div>
                {/if}
            {:else}
                <div class="flex md:flex-row flex-col w-full md:space-x-4 md:space-y-0 space-y-4 mb-4 justify-center">
                    <div class="w-full p-4 border-black border rounded-lg bg-white text-black max-w-lg"><h4>{conf.account.not_a_member}</h4></div>
                </div>
                <div class="flex md:flex-row flex-col w-full md:space-x-4 md:space-y-0 space-y-4 justify-center">
                    <Button to={conf.pages.subscribe.route} size="medium" cls="w-full max-w-lg">{conf.account.subscribe}</Button>
                </div>
            {/if}
            </div>
            <div class="flex flex-col md:p-8 p-6 pb-8 pt-8 md:pb-10 mb-8 rounded-lg bg-neutral-800">
                <h2 class="font-futurar md:text-2xl text-xl mb-4">{conf.account.notifications}</h2>
                <div class="flex md:flex-row flex-col w-full md:space-x-4 md:space-y-0 space-y-4 mb-4">
                    <ButtonChoice cls="w-full" on:click={()=>{changePrefEmail("new_book", $emailPrefNewBook);}} disable={disableButtonsEmailPref} selected={$emailPrefNewBook}>{conf.account.new_book}</ButtonChoice>
                    <ButtonChoice cls="w-full" on:click={()=>{changePrefEmail("ref_someone", $emailPrefRefSomeone);}} disable={disableButtonsEmailPref} selected={$emailPrefRefSomeone}>{conf.account.referral}</ButtonChoice>
                </div>
                <div class="flex md:flex-row flex-col w-full md:space-x-4 md:space-y-0 space-y-4">
                    <ButtonChoice cls="w-full" on:click={()=>{changePrefEmail("sub_will_expire", $emailPrefSubWillExpire);}} disable={disableButtonsEmailPref} selected={$emailPrefSubWillExpire}>{conf.account.membership_expiration}</ButtonChoice>
                    <ButtonChoice cls="w-full" on:click={()=>{changePrefEmail("promo", $emailPrefPromo);}} disable={disableButtonsEmailPref} selected={$emailPrefPromo}>{conf.account.ads}</ButtonChoice>
                </div>
            </div>
            <div class="flex flex-col md:p-8 pb-8 pt-8 mb-8 md:space-x-4 md:space-y-0 space-y-4 rounded-lg bg-neutral-800">
                <Link to={conf.pages.delete_account.route} cls="text-xl hover:underline">{conf.pages.delete_account.title}</Link>
            </div>
        </div>
    </div>
</div>
<Footer></Footer>