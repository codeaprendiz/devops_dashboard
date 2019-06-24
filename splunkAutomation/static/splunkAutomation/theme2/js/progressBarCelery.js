function updateProgress (progressUrl) {
    fetch(progressUrl).then(function(response) {
        response.json().then(function(data) {
            // update the appropriate UI components
            setProgress(data.state, data.details);
            setTimeout(updateProgress, 500, progressUrl);
        });
    });
}