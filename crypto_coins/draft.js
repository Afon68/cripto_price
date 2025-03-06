document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll(".token-button");
    
    buttons.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();  // Отменяем стандартное действие <a>
            
            const tokenSymbol = this.getAttribute("data-symbol");  // Получаем символ токена
            
            console.log(`Выбран токен: ${tokenSymbol}`);  // Для отладки

            // Делаем запрос на API
            fetch(`/latest-price-list/${tokenSymbol}`)
                .then(response => response.json())
                .then(data => {
                    console.log(data);  // Посмотрим, что приходит в ответе
                    
                    if (data.price_list !== "Нет списка данных") {
                        updatePriceTable(data.price_list);  // Обновляем таблицу
                    } else {
                        alert("Нет данных для этого токена!");
                    }
                })
                .catch(error => console.error("Ошибка загрузки данных:", error));
        });
    });
});

// Функция обновления таблицы цен
function updatePriceTable(priceList) {
    const table = document.getElementById("table-container");
    table.innerHTML = "<tr><th>Время</th><th>Цена</th><th>Изменение</th></tr>";  // Очищаем таблицу
    
    priceList.forEach(item => {
        const row = `<tr>
            <td>${item.timestamp}</td>
            <td>${item.price}</td>
            <td>${item.direction} ${item.diff !== null ? item.diff : "-"}</td>
        </tr>`;
        table.innerHTML += row;
    });

    console.log("✅ Таблица обновлена!");
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////

document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll(".token-button");
    const firstToken = buttons.length > 0 ? buttons[0].getAttribute("data-symbol") : null;  // Берём первый токен

    if (firstToken) {
        fetchData(firstToken);  // Загружаем данные при старте
    }

    buttons.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();  // Отключаем переход по ссылке
            
            const tokenSymbol = this.getAttribute("data-symbol");
            fetchData(tokenSymbol);  // Загружаем данные для нового токена
        });
    });
});

// 📌 Функция для загрузки данных
function fetchData(tokenSymbol) {
    console.log(`🔍 Загружаем данные для: ${tokenSymbol}`);

    fetch(`/latest-price-list/${tokenSymbol}`)
        .then(response => response.json())
        .then(data => {
            console.log("📊 Данные:", data);

            if (data.price_list !== "Нет списка данных") {
                updatePriceTable(data.price_list);
            } else {
                alert("Нет данных для этого токена!");
            }
        })
        .catch(error => console.error("❌ Ошибка загрузки данных:", error));
}

// 📌 Функция обновления таблицы
function updatePriceTable(priceList) {
    const table = document.getElementById("table-container");
    table.innerHTML = "<tr><th>Время</th><th>Цена</th><th>Изменение</th></tr>";  // Очищаем таблицу
    
    priceList.forEach(item => {
        const row = `<tr>
            <td>${item.timestamp}</td>
            <td>${item.price}</td>
            <td>${item.direction} ${item.diff !== null ? item.diff : "-"}</td>
        </tr>`;
        table.innerHTML += row;
    });

    console.log("✅ Таблица обновлена!");
}


let chartInstance = null;  // Храним текущий график

function updateTokenChart(getData) {
    console.log(`TokenCharttokenSymbol = ${tokenSymbol}`)
    const token_name = getData.price_list[0].name;
    console.log(`TokenChart_token_name = ${token_name}`)

    const ctx = document.getElementById('tokenChart').getContext('2d');

    const labels = getData.price_list.map(entry => entry.timestamp);  // Метки оси X (время)
    const prices = getData.price_list.map(entry => entry.price);  // Данные оси Y (цены)

    if (chartInstance === null) {
        console.log("✅ Создаём новый график!");
        chartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: `${token_name} Price (USD)`,
                    data: prices,
                    borderColor: "blue",  
                    backgroundColor: "rgba(0, 0, 255, 0.1)",  
                    tension: 0.3  // ✅ Делаем линии плавными
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: 1000,  // ✅ Плавное обновление (1 сек)
                    easing: 'easeInOutQuad'
                },
                scales: {
                    x: {
                        ticks: {
                            autoSkip: true,  // Автоматическое скрытие лишних подписей на оси X
                            maxTicksLimit: 10
                        }
                    },
                    y: {
                        beginAtZero: false  // ✅ График без резкого старта с 0
                    }
                }
            }
        });
    } else {
        console.log("🔄 Обновляем график...");
        chartInstance.data.labels = labels;
        chartInstance.data.datasets[0].label = `${token_name} Price (USD)`;
        chartInstance.data.datasets[0].data = prices;
        chartInstance.update();  // ✅ Плавное обновление без перерисовки
    }
}
