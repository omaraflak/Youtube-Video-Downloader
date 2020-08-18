const onDownloadClicked = () => {
    let videoId = window.location.search.split('v=')[1]
    let ampersandPosition = videoId.indexOf('&')
    if(ampersandPosition != -1) {
        videoId = videoId.substring(0, ampersandPosition)
    }

    fetch(`http://localhost:8080/start/?id=${videoId}`)
        .then(response => response.json())
        .then(data => {
            const taskId = data.task_id
            if (taskId) {
                window.open(`http://localhost:8080/view/?task_id=${taskId}`, '_blank')
            }
        })
        .catch(error => {
            console.log(error)
        })
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
