chrome.contextMenus.removeAll();
chrome.contextMenus.create({
    title: "Terly",
    contexts: ["image"],
    onclick: function (info, tab) {
        chrome.downloads.download({url: info.srcUrl, filename: "terly_photo.png"});
        chrome.tabs.create({
            url: "http://127.0.0.1:5000/"
        });
    }
});