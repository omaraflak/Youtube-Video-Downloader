const SERVER = 'http://localhost:8080'

let videoFormats = []

const getVideoId = () => {
    let videoId = window.location.search.split('v=')[1]
    let ampersandPosition = videoId.indexOf('&')
    if (ampersandPosition != -1) {
        videoId = videoId.substring(0, ampersandPosition)
    }
    return videoId
}

const fetchVideoFormats = () => {
    const videoId = getVideoId()
    chrome.runtime.sendMessage({uri: 'info', url: `${SERVER}/info/?id=${videoId}`})
}

const onFormatClicked = event => {
    const formatId = event.target.id
    const videoId = getVideoId()
    chrome.runtime.sendMessage({uri: 'start', url: `${SERVER}/start/?id=${videoId}&format=${formatId}`})
}

const showFormatSelectionPopup = () => {
    const buttonsHtml = videoFormats.map(format => {
        return `<button id='${format.id}' class='format-button'>${format.format}</button>`
    }).join('</br>')

    Swal.fire({
        title: 'Select a format',
        icon: 'question',
        html: buttonsHtml,
        showCloseButton: true,
        showConfirmButton: false,
        onOpen: () => {
            videoFormats.forEach(format => {
                document.getElementById(format.id).onclick = event => {
                    swal.close()
                    onFormatClicked(event)
                }
            })
        }
    })
}

const injectCode = code => {
    const contents = document.querySelector("#meta-contents")
    if (contents == null) {
        return false
    }
    const topRow = contents.querySelector('#top-row')
    if (topRow == null) {
        return false
    }
    topRow.appendChild(code)
}

const injectButton = () => {
    const downloadButton = document.createElement('button')
    downloadButton.classList.add('download-button')
    downloadButton.innerHTML = 'DOWNLOAD'
    downloadButton.onclick = showFormatSelectionPopup

    const injectLoop = () => {
        if (!injectCode(downloadButton)) {
            setTimeout(injectLoop, 1500)
        }
    }

    injectLoop()
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.uri == 'start') {
        const taskId = request.response.task_id
        window.open(`${SERVER}/view/?task_id=${taskId}`, '_blank')
    } else if (request.uri == 'info') {
        videoFormats = request.response
        injectButton()
    }
})

window.onload = () => {
    fetchVideoFormats()
}
