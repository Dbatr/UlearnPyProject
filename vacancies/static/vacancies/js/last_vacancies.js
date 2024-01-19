document.addEventListener('DOMContentLoaded', function () {
    var vacancyTitles = document.querySelectorAll('.vacancy-title');

    vacancyTitles.forEach(function (title) {
        title.addEventListener('click', function () {
            var vacancyId = this.getAttribute('data-vacancy-id');
            var detailsContainer = document.getElementById('details-' + vacancyId);

            if (detailsContainer.style.display === 'none' || detailsContainer.style.display === '') {
                detailsContainer.style.display = 'block';
                this.classList.add('expanded');
            } else {
                detailsContainer.style.display = 'none';
                this.classList.remove('expanded');
            }
        });
    });
});
