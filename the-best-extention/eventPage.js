chrome.contextMenus.removeAll();
chrome.contextMenus.create({
      title: "first",
      contexts: ["image"],
      onclick: function(info, tab) {
          chrome.tabs.create({
              url: "http://127.0.0.1:5000/"
          });
      }
});