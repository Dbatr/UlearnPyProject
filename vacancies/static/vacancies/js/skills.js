// Инициализация значением по умолчанию при загрузке страницы
document.getElementById('selectedYear').innerText = 'ТОП-20 навыков за {{ unique_years.0 }}';

function filterByYear() {
    var selectedYear = document.getElementById('year').value;
    var allRows = document.querySelectorAll('.year-row');

    // Скрыть все строки
    allRows.forEach(function (row) {
        row.style.display = 'none';
    });

    // Показать строки, соответствующие выбранному году
    var selectedYearRows = document.querySelectorAll('.year-' + selectedYear);
    selectedYearRows.forEach(function (row) {
        row.style.display = '';
    });

    // Обновить отображаемый год
    document.getElementById('selectedYear').innerText = 'ТОП-20 навыков за ' + selectedYear;
}

// Запуск фильтрации при загрузке страницы
filterByYear();


// Инициализация значением по умолчанию при загрузке страницы
document.getElementById('selectedBackendYear').innerText = 'ТОП-20 навыков за {{ unique_backend_years.0 }}';

function filterBackendByYear() {
    var selectedBackendYear = document.getElementById('backend-year').value;
    var allBackendRows = document.querySelectorAll('.backend-year-row');

    // Скрыть все строки
    allBackendRows.forEach(function (row) {
        row.style.display = 'none';
    });

    // Показать строки, соответствующие выбранному году
    var selectedBackendYearRows = document.querySelectorAll('.backend-year-' + selectedBackendYear);
    selectedBackendYearRows.forEach(function (row) {
        row.style.display = '';
    });

    // Обновить отображаемый год
    document.getElementById('selectedBackendYear').innerText = 'ТОП-20 навыков за ' + selectedBackendYear;
}

// Запуск фильтрации при загрузке страницы
filterBackendByYear();