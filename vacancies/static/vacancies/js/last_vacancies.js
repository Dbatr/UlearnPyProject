document.addEventListener('DOMContentLoaded', function () {
    var showDetailsButtons = document.querySelectorAll('.show-details');

    showDetailsButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            var vacancyId = this.getAttribute('data-vacancy-id');
            var detailsContainer = document.getElementById('details-' + vacancyId);

            if (detailsContainer.style.display === 'none' || detailsContainer.style.display === '') {
                detailsContainer.style.display = 'block';
            } else {
                detailsContainer.style.display = 'none';
            }
        });
    });
});