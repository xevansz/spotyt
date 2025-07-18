document.addEventListener('DOMContentLoaded', function() {
    console.log('Spotify app is ready');
    var form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function() {
            var spinner = document.createElement('div');
            spinner.className = 'spinner';
            form.appendChild(spinner);
        });
    }
});