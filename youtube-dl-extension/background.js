chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    fetch(request.url)
        .then(response => response.json())
        .then(response => {
            chrome.tabs.query({active: true, currentWindow: true}, tabs => {
                chrome.tabs.sendMessage(tabs[0].id, {...request, response})
            })
        })
        .catch(error => {
            console.log(error)
        })
})
