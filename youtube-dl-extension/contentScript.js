const onDownloadClicked = () => {
    let videoId = window.location.search.split('v=')[1]
    let ampersandPosition = videoId.indexOf('&')
    if(ampersandPosition != -1) {
        videoId = videoId.substring(0, ampersandPosition)
    }
    const downloadLink = `http://localhost:8080/download/?id=${videoId}`
    window.open(downloadLink, '_blank')
}

const injectCode = (code) => {
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

window.onload = () => {
    const downloadButton = document.createElement('button')
    downloadButton.classList.add('download-button')
    downloadButton.innerHTML = 'DOWNLOAD'
    downloadButton.onclick = onDownloadClicked

    const injectLoop = () => {
        if (!injectCode(downloadButton)) {
            setTimeout(injectLoop, 1500)
        }
    }

    injectLoop()
}
