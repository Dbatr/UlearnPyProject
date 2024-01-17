document.addEventListener('DOMContentLoaded', function () {
    // Получаем ссылки на элементы
    const sitename = document.querySelector('.sitename');
    const logo = document.querySelector('.logo');

    // Добавляем обработчик события клика для h1
    sitename.addEventListener('click', function () {
        location.reload();
    });

    // Добавляем обработчик события клика для img
    logo.addEventListener('click', function () {
        location.reload();
    });
});
