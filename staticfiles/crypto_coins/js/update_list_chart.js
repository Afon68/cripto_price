let tokenSymbol = null;  // Токен по умолчанию
let timeFrame;
let timePeriod;
// Функция для навешивания обработчиков событий
function clickButton() {
    console.log("✅ Работает clickButton");
    const buttons_time = document.querySelectorAll(".token-button");
    buttons_time.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();  // Отменяем стандартное действие <a>
            tokenSymbol = this.getAttribute("data-symbol");  // Получаем символ токена
            console.log(`🔹 Выбран токен: ${tokenSymbol}`);
            saveSelectedToken();
            fetchData();  // Загружаем данные для нового токена
        });
    });
    const buttons_frame = document.querySelectorAll(".frame-button");
    buttons_frame.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();  // Отменяем стандартное действие <a>
            timeFrame = this.getAttribute("data-frame");  // Получаем символ токена
            console.log(`🔹 Выбран frame: ${timeFrame}`);
            saveSelectedFrame()
            fetchData();  // Загружаем данные для нового токена
        });
    });
   
    const buttons_period = document.querySelectorAll(".period-button");
    buttons_period.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();  // Отменяем стандартное действие <a>
            timePeriod = this.getAttribute("data-period");  // Получаем символ токена
            console.log(`🔹 Выбран Period: ${timePeriod}`);
            saveSelectedPeriod()
            fetchData();  // Загружаем данные для нового токена
        });
    });
    fetchData()
    console.log(`🔹 Текущий токен: ${tokenSymbol}`);
    // console.log(`🔹 Текущий токен: ${timeFrame}`);
}
///////////////////clickButton() finish /////////////////////////////////////////////////////////////////////////

////////////////Начало работы файла/////////////////////////////////////////////////////////////////////////////
// Ждём, пока DOM загрузится
document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ DOM загружен!");
    // Сохранение tokenSymbol, timeFrame, timePeriod в localStorage(хранилище браузера)
    savedToken = localStorage.getItem("selectedToken")
    if (savedToken) {
        tokenSymbol = savedToken;  // Устанавливаем сохранённый токен
        console.log(`✅ Загруженный токен: ${tokenSymbol}`);
    } else {
        console.log(`⚠️ Токен не найден в localStorage, выбираем стандартный`);
        tokenSymbol = "BTC"
    }

    savedFrame = localStorage.getItem("selectedFrame")
    if (savedFrame) {
        timeFrame = savedFrame;  // Устанавливаем сохранённый токен
        console.log(`✅ Загруженный Time-Frame: ${timeFrame}`);
    } else {
        console.log(`⚠️ Time-Frame не найден в localStorage, выбираем стандартный`);
        timeFrame = 30
    }

    savedPeriod = localStorage.getItem("selectedPeriod")
    if (savedPeriod) {
        timePeriod = savedPeriod;  // Устанавливаем сохранённый токен
        console.log(`✅ Загруженный Time-Period: ${timePeriod}`);
        clickButton()
    } else {
        console.log(`⚠️ Период не найден в localStorage, выбираем стандартный`);
        timePeriod = 24
        clickButton()
    }


    // чтобы по умолчанию была светлая тема(если не надо, можно закоментить)
    document.body.classList.remove("dark-mode");
    // localStorage.removeItem("selectedToken"); // Удаляем сохранённое значение


    // 🔄 Проверяем, была ли тёмная тема раньше
    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark-mode");
    }

    document.getElementById("theme-toggle").addEventListener("click", function () {
        document.body.classList.toggle("dark-mode");
        // 💾 Сохраняем тему в localStorage
        if (document.body.classList.contains("dark-mode")) {
            localStorage.setItem("theme", "dark");
        } else {
            localStorage.setItem("theme", "light");
        }
    })
});
// Обновление данных каждую минуту
setInterval(() => {
    fetchData();
}, 60000);


function fetchData() {

    console.log(`🔍 Загружаем данные для: ${tokenSymbol}/${timeFrame}/${timePeriod}/`);  // /${timeFrame}
    fetch(`/latest-price-list/${tokenSymbol}/${timeFrame}/${timePeriod}/`)  // ✅ Запрашиваем список цен   /${timeFrame}
        .then(response => response.json())
        .then(data => {
            console.log(`Данные = ${data.price_list}`);  // в data два объекта price_list(цены за сутки по одному токену) и last_all_price(последние цены для каждой валюты)
            const latestData = data.last_all_price;  // последние цены для каждой валюты
            let title = document.querySelector("title");  // Получаем таблицу
            title.innerText = tokenSymbol

            let coin = document.getElementById("coin");     // favor
            // coin.innerText = data.price_list[0].name
            coin.src = `https://bin.bnbstatic.com/static/assets/logos/${tokenSymbol}.png`

            let favor = document.getElementById("favor");
            favor.innerText = data.price_list[0].name

            let frame = document.getElementById("frame");
            if (frame) {
                frame.innerText = timeFrame < 50 ? timeFrame + " min" : "1 hour"
            } else {
                console.error("❌ Ошибка: Element frame не найден!");
            }
            let period = document.getElementById("period");
            period.innerText = timePeriod === 1 ? "1 hour" : timePeriod + "hours"

            let table = document.querySelector("table");  // Получаем таблицу
            table.innerHTML = `
                <tr>
                    <th>Time</th>
                    <th>Price(USD)</th>
                    <th>Change</th>
                </tr>`;  // Очищаем старые данные и добавляем заголовки
            
            let token_name = data.price_list[0].name;
            let latest_price = data.price_list[0].price;
            let previous_price = data.price_list[1]?.price || latest_price;  // Подстраховка
            let current = document.getElementById("current");
            if (current) {
                if (latestData) {
                    latestData.forEach(token => {
                        if (token.name === token_name) {
                            current.innerText = `Current ${token_name} Price: ${token.price} USD ${(token.dif > 0 ? "↑" : "↓")}`;
                            current.style.color = token.dif > 0 ? "green" : "red";
                        }
                    })
                }

            } else {
                console.error("❌ Ошибка: priceElement или current не найден!");
            }

            let history = document.getElementById("history-price");
            history.innerText = `${token_name} Price History `

            for (let elem of data.price_list) {
                let row = table.insertRow(-1);  // Добавляем новую строку
                row.insertCell(0).innerText = convertISOToLocal(elem.timestamp);  // Время
                let priceCell = row.insertCell(1)
                priceCell.innerHTML = elem.price + "  " + elem.direction;  // Цена + стрелка (HTML)
                let diffCell = row.insertCell(2);
                diffCell.innerText = elem.diff !== null ? elem.diff : "—";  // Разница

                if (elem.diff > 0) {
                    priceCell.style.color = "green";
                    diffCell.style.color = "green";  // Если положительное значение — зелёный

                } else if (elem.diff < 0) {
                    diffCell.style.color = "red";  // Если отрицательное значение — красный
                    priceCell.style.color = "red";
                } else {
                    diffCell.style.color = "blue";  // Если нет изменений — чёрный
                    priceCell.style.color = "blue";  // Если нет изменений — чёрный
                }
            }
            updatechartInstance(data)
            currentAllPrice(latestData)
        })
        .catch(error => console.error('Ошибка загрузки данных:', error))
}

let chartInstance = null;  // Храним текущий график

function updatechartInstance(getData) {
    console.log(`chartInstancetimeSymbol = ${tokenSymbol}`)
    const token_name = getData.price_list[0].name;
    console.log(`chartInstance_time_name = ${token_name}`)

    const ctx = document.getElementById('tokenChart').getContext('2d');
    // console.log(`ctx = ${document.getElementById('chartInstance')}`)

    const labels = getData.price_list.reverse().map(entry => convertISOToLocal(entry.timestamp));
    // var result = string .replace(/20|,/gi, () => "");   // Метки оси X (время)
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
                    borderColor: "gray",  // Базовый цвет линии
                    backgroundColor: "rgba(0, 0, 255, 0.1)",
                    borderWidth: 2, // Базовая толщина
                    fill: true,
                    pointRadius: 0.5, // Радиус точек
                    tension: 0.3,  // ✅ Делаем линии плавными
                    segment: {
                        borderColor: ctx => {
                            const chart = ctx.chart;
                            const { data } = chart.data.datasets[0];
                            const index = ctx.p1DataIndex;  // Индекс текущей точки

                            // Если нет предыдущей точки, оставляем серый цвет
                            if (index === 0) return "gray";

                            // Меняем цвет линии в зависимости от направления
                            return data[index] > data[index - 1] ? "green" : "red";
                        },
                        borderWidth: ctx => {
                            const chart = ctx.chart;
                            const { data } = chart.data.datasets[0];
                            const index = ctx.p1DataIndex;

                            // Если нет предыдущей точки, оставляем стандартную толщину
                            if (index === 0) return 2;

                            // Толстая линия при росте, тонкая при падении
                            return data[index] < data[index - 1] ? 2 : 2;
                        }

                    }
                }]
            },
            options: {
                responsive: true,
                // maintainAspectRatio: false,
                animation: {
                    duration: 1000,  // ✅ Плавное обновление (1 сек)
                    // easing: 'easeInOutQuad'
                },
                scales: {
                    x: {
                        ticks: {
                            autoSkip: true,  // Автоматическое скрытие лишних подписей на оси X
                            maxTicksLimit: 10,
                        },
                        title: { display: true, text: "Date  Time" }
                    },
                    y: {
                        beginAtZero: false,  // ✅ График без резкого старта с 0
                        title: { display: true, text: "Price (USD)" }
                    }
                }
            }
        });
        const sortedPrices = getData.price_list;
        // красим сегменты(звенья) графика и фон под ними
        chartInstance.data.datasets[0].segment = {
            borderColor: ctx => {
                const index = ctx.p1DataIndex; // Индекс второй точки сегмента
                if (!index || index === 0) return "gray"; // Первая точка — серая
                return chartInstance.data.datasets[0].data[index] > chartInstance.data.datasets[0].data[index - 1]
                    ? "green"  // 📈 Если цена растёт — зелёный
                    : "red";    // 📉 Если падает — красный
            },
            backgroundColor: ctx => {
                const index = ctx.p1DataIndex;
                if (!index || index === 0) return "rgba(128, 128, 128, 0.1)"; // Серый, если первая точка
                return chartInstance.data.datasets[0].data[index] > chartInstance.data.datasets[0].data[index - 1]
                    ? "rgba(0, 255, 0, 0.1)"  // 📈 Зелёная прозрачность
                    : "rgba(255, 0, 0, 0.1)";  // 📉 Красная прозрачность
            }
        };
        // цвет межзвеньевой точки
        chartInstance.data.datasets[0].borderColor = sortedPrices.map((priceData, i) => {
            if (i === 0) return "blue";
            return sortedPrices[i].price > sortedPrices[i - 1].price ? "green" : "red";
        });
        chartInstance.data.datasets[0].pointBackgroundColor = sortedPrices.map((priceData, i) => {
            if (i === 0) return "green";
            return sortedPrices[i].price > sortedPrices[i - 1].price ? "green" : "red";
        });
        //размер межзвеньевой точки
        chartInstance.data.datasets[0].borderWidth = sortedPrices.map((priceData, i) => {
            if (i === 0) return 2;
            return sortedPrices[i].price > sortedPrices[i - 1].price ? 2 : 2;
        });
        chartInstance.update()
    } else {
        console.log("🔄 Обновляем график...");
        //labels
        chartInstance.data.labels = labels
        chartInstance.data.datasets[0].label = `${token_name} Price (USD)`;
        chartInstance.data.datasets[0].data = prices
        chartInstance.update();  // ✅ Плавное обновление без перерисовки
    }
}

function currentAllPrice(latestData) {
    let tickerContainer = document.querySelector("#all-price");
   

    if (!tickerContainer) return;

    let tickerHTML = latestData.map(token => {
        let color = token.dif > 0 ? "green" : "red";
        let percentColor = token.price_change_percentage > 0 ? "green" : "red";
        
        return `
            <p class="ticker-item">
                <img class="icon" src="${token.url_icon}" alt="...">
                <span class="token-name" style="color:${color}">${token.name} ${token.price} ${token.dif > 0 ? '↑' : '↓'}</span>
                <span class="proc" style="color:${percentColor}">${token.price_change_percentage > 0 ? `+${token.price_change_percentage}%` : `${token.price_change_percentage}%`}</span>
            </p>
        `;
    }).join("");
    
    tickerContainer.innerHTML = tickerHTML + tickerHTML;
    // Убеждаемся, что блок тянется шире экрана
    const tickerWidth = tickerContainer.scrollWidth;
    tickerContainer.style.minWidth = `${tickerWidth}px`;

}
// функция для конвертации времени в UTC (например, 2025-03-12T18:45:49Z)  в часовой пояс пользователя
function convertISOToLocal(isoString) {
    console.log(`isoString = ${isoString}`);
    let date = new Date(isoString);
    timeLable = date.toLocaleString()
    return timeLable.slice(0,6) + timeLable.slice(8,10) + timeLable.slice(11); 
}

//функции для сохранения данных, которые были перед перезагрузкой
// Токен
function saveSelectedToken() {
    localStorage.setItem("selectedToken", tokenSymbol);
    console.log(`✅${tokenSymbol} сохранен в localStorage`)
}

//time-frame
function saveSelectedFrame() {
    localStorage.setItem("selectedFrame", timeFrame);
    console.log(`✅${timeFrame} сохранен в localStorage`)
}

// time-period
function saveSelectedPeriod() {
    localStorage.setItem("selectedPeriod", timePeriod);
}






