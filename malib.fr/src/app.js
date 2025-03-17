import * as conf from "./app.json";
import { writable } from "svelte/store";

export const params = writable(new Proxy(new URLSearchParams(window.location.search), { get: (searchParams, prop) => searchParams.get(prop)}))
export const currentRoute = writable(window.location.pathname);
export const registerEmail = writable("");
export const isLogged = writable(false);
export const isSub = writable(false);
export const isDiscount = writable(false);
export const isSubCanceled = writable(false);
export const subSince = writable(null);
export const subCurrentPeriodEnd = writable(null);
export const nextCreditDate = writable(null);
export const setPref = writable(false);
export const pickFirstBook = writable(false);
export const bookCredit = writable(0);
export const unreadNotifications = writable(0);
export const settingReaderFont = writable("FUTURA");
export const settingReaderZoom = writable(130);
export const settingReaderTheme = writable("DGREY");
export const settingLibrarySorting = writable("ACTIVITY");
export const emailPrefNewBook = writable(false);
export const emailPrefRefSomeone = writable(false);
export const emailPrefSubWillExpire = writable(false);
export const emailPrefPromo = writable(false);
export const referralCode = writable("");
export const email = writable("");
export const networkFailed = writable(false);
export const cacheLibrary = writable(null);

export async function clearParams(newParams=""){
    window.history.replaceState({}, "", window.location.pathname + newParams);
}

export function goTo(path){
    window.scrollTo(0,0);
    let urlArray = path.split("?");
    currentRoute.set(urlArray[0]);
    params.set(new Proxy(new URLSearchParams(urlArray[1]), { get: (searchParams, prop) => searchParams.get(prop)}))
    window.history.pushState({path: urlArray[0]}, "", window.location.origin + path);
}

export async function api(endpoint, method, params, body){
    try{
        let headers = {"Content-Type": "application/json"};

        if(localStorage.getItem("at"))
            headers.Authorization = "Bearer " + localStorage.getItem("at");

        const url = new URL(conf.api_url + endpoint);
        url.search = new URLSearchParams(params);
        let request = {method:method, headers:headers}
        if(method !== "get" && method !== "head")
            request.body = JSON.stringify(body)
        const response = await fetch(url, request);
        const data = await response.json();
        const status = response.status;

        if("access_token" in data)
            localStorage.setItem("at", data.access_token);

        if(status === 444 && localStorage.getItem("at"))
            logout();

        return {status:status, data:data};
    }
    catch(e){networkFailed.set(true)}
}

export function clickOutside(node, onEventFunction) {
    const handleClick = event => {
        let path = event.composedPath();
        if(!path.includes(node))
            onEventFunction();
    }
    document.addEventListener("click", handleClick);
    return {destroy(){document.removeEventListener("click", handleClick);}}
}

export function setReferrer(ref){
    localStorage.setItem("ref", ref);
}

export function getReferrer(){
    return localStorage.getItem("ref");
}

export async function updateAuthInfo(){
    try{
        let resp = await api("/auth-info", "get", {}, {});
        networkFailed.set(false);
        if(resp.status === 200){
            isLogged.set(true);
            isSub.set(resp.data.steps.is_sub);
            isDiscount.set(resp.data.sub_discount);
            isSubCanceled.set(resp.data.sub_cancel_at_period_end);
            if(resp.data.sub_since)
                subSince.set(new Date(resp.data.sub_since));
            else
                subSince.set(null);
            if(resp.data.sub_current_period_end)
                subCurrentPeriodEnd.set(new Date(resp.data.sub_current_period_end));
            else
                subCurrentPeriodEnd.set(null);
            if(resp.data.next_credit_date)
                nextCreditDate.set(new Date(resp.data.next_credit_date));
            else
                nextCreditDate.set(null);
            setPref.set(resp.data.steps.set_pref);
            pickFirstBook.set(resp.data.steps.pick_first_book);
            bookCredit.set(resp.data.book_credit);
            settingReaderFont.set(resp.data.settings.reader_font);
            settingReaderZoom.set(resp.data.settings.reader_zoom);
            settingReaderTheme.set(resp.data.settings.reader_theme);
            settingLibrarySorting.set(resp.data.settings.library_sorting);
            emailPrefNewBook.set(resp.data.email_preferences.new_book);
            emailPrefRefSomeone.set(resp.data.email_preferences.ref_someone);
            emailPrefSubWillExpire.set(resp.data.email_preferences.sub_will_expire);
            emailPrefPromo.set(resp.data.email_preferences.promo);
            unreadNotifications.set(resp.data.unread_notifications);
            referralCode.set(resp.data.referral_code);
            email.set(resp.data.email);
        }
        else if(resp.status === 444 || resp.status === 404)
            authInfoInit();
    }catch(e){networkFailed.set(true)}
}

export function logout(){
    localStorage.removeItem("at");
    authInfoInit();
}

export function removeAccent(str){
    return str
            .replace(/[áàãâä]/gi,"a")
            .replace(/[éèëê]/gi,"e")
            .replace(/[íìïî]/gi,"i")
            .replace(/[óòöôõ]/gi,"o")
            .replace(/[úùüû]/gi, "u")
            .replace(/[ç]/gi, "c")
            .replace(/[ñ]/gi, "n");
    }

function authInfoInit(){
    isLogged.set(false);
    isSub.set(false);
    isDiscount.set(false);
    isSubCanceled.set(false);
    subSince.set(null);
    subCurrentPeriodEnd.set(null);
    nextCreditDate.set(null);
    setPref.set(false);
    pickFirstBook.set(false);
    bookCredit.set(0);
    settingReaderFont.set("FUTURA");
    settingReaderZoom.set(80);
    settingReaderTheme.set("DGREY");
    settingLibrarySorting.set("ACTIVITY");
    emailPrefNewBook.set(false);
    emailPrefRefSomeone.set(false);
    emailPrefSubWillExpire.set(false);
    emailPrefPromo.set(false);
    unreadNotifications.set(0);
    referralCode.set("");
    email.set("");
    cacheLibrary.set(null);
}
