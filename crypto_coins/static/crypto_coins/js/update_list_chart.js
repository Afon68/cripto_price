let tokenSymbol = null;  // Токен по умолчанию
let timeFrame;
let timePeriod;
// Функция для навешивания обработчиков событий
function clickButton() {
    console.log("✅ Работает clickButton");

    const buttons_time = document.querySelectorAll(".token-button");

    if (buttons_time.length > 0) {
        tokenSymbol = buttons_time[1].getAttribute("data-symbol");  // Берём первый токен
        // fetchData();  // Загружаем данные при старте
    }

    buttons_time.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();  // Отменяем стандартное действие <a>
            tokenSymbol = this.getAttribute("data-symbol");  // Получаем символ токена
            console.log(`🔹 Выбран токен: ${tokenSymbol}`);
            fetchData();  // Загружаем данные для нового токена
        });
    });
    const buttons_frame = document.querySelectorAll(".frame-button");

    if (buttons_frame.length > 0) {
        timeFrame = buttons_frame[3].getAttribute("data-frame");  // Берём первый токен
        // fetchData();  // Загружаем данные при старте
    }

    buttons_frame.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();  // Отменяем стандартное действие <a>
            timeFrame = this.getAttribute("data-frame");  // Получаем символ токена
            console.log(`🔹 Выбран frame: ${timeFrame}`);
            fetchData();  // Загружаем данные для нового токена
        });
    });

    const buttons_period = document.querySelectorAll(".period-button");

    if (buttons_period.length > 0) {
        timePeriod = buttons_period[1].getAttribute("data-period");
        console.log(`🔹 Time Period: ${timePeriod}`); // Берём первый токен
        fetchData();  // Загружаем данные при старте
    }

    buttons_period.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();  // Отменяем стандартное действие <a>
            timePeriod = this.getAttribute("data-period");  // Получаем символ токена
            console.log(`🔹 Выбран Period: ${timePeriod}`);
            fetchData();  // Загружаем данные для нового токена
        });
    });
    console.log(`🔹 Текущий токен: ${tokenSymbol}`);
    // console.log(`🔹 Текущий токен: ${timeFrame}`);
}

// Ждём, пока DOM загрузится
document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ DOM загружен!");
    // let current = document.getElementById("current");
    // console.log("🔍 Найден элемент:", current); // Проверяем, найден ли элемент

    // if (current) {
    //     current.innerText = "Загрузка цены..."; // Временно ставим заглушку
    //     current.style.color = "gray";
    // } else {
    //     console.error("❌ Ошибка: элемент с id='current' не найден!");
    // }

    clickButton();  // Запускаем обработчик кнопок
});



// Дополнительно, если нужно вызвать через `setTimeout`
// setTimeout(() => {
//     console.log("⏳ Запуск через 500 мс...");
//     clickButton();
// }, 500);

// Обновление данных каждую минуту
setInterval(() => {
    fetchData();
}, 60000);

// clickButton()
// setInterval(fetchData, 60000);

// setInterval(clickButton, 60000);  // 🔄 Обновляем цену каждые 5 секунд
// clickButton()  // 🔥 Запускаем сразу при загрузке страниц

function fetchData() {

    console.log(`🔍 Загружаем данные для: ${tokenSymbol}/${timeFrame}/${timePeriod}/`);  // /${timeFrame}
    fetch(`/latest-price-list/${tokenSymbol}/${timeFrame}/${timePeriod}/`)  // ✅ Запрашиваем список цен   /${timeFrame}
        .then(response => response.json())
        .then(data => {
            console.log(`Данные = ${data.price_list}`);  // в data два объекта price_list(цены за сутки по одному токену) и last_all_price(последние цены для каждой валюты)
            const latestData = data.last_all_price;  // последние цены для каждой валюты
            let title = document.querySelector("title");  // Получаем таблицу
            title.innerText = tokenSymbol

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
            // ✅ Получаем **самую последнюю цену**
            // let latest_price = data.price_list[0].price;
            // let previous_price = data.price_list[1].price;

            // // ✅ Отображаем текущую цену
            // let priceElement = document.getElementById("eth-price");
            // priceElement.innerText = latest_price + " USD " + (latest_price > previous_price ? "↑" : "↓");
            // priceElement.style.color = latest_price > previous_price ? "green" : "red";
            let token_name = data.price_list[0].name;
            //let current = document.getElementById("current") ; // Получаем таблицу
            // // current.innerText = time_name;
            //current.innerText = "Текущая статья:";
            //current.style.color = latest_price > previous_price ? "green" : "red";
            //current
            let latest_price = data.price_list[0].price;
            let previous_price = data.price_list[1]?.price || latest_price;  // Подстраховка

            // let priceElement = document.getElementById("eth-price");
            let current = document.getElementById("current");
            // priceElement.innerText = latest_price + " USD " + (latest_price > previous_price ? "↑" : "↓");
            // priceElement.style.color = latest_price > previous_price ? "green" : "red";
            if (current) {
                if (latestData) {
                    latestData.forEach(token => {
                        if(token.name === token_name) {
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
            // let current = document.getElementById("current");
            // console.log("🔍 Найден элемент:", current); // Проверяем, найден ли элемент

            // if (current) {
            //     current.innerText = "Текущая цена Bitcoin:";
            //     current.style.color = "green";
            // } else {
            //     console.error("❌ Ошибка: элемент с id='current' не найден!");
            // }


            // if (data.price_list.length > 0) {
            //     let time_name = data.price_list[0].name || "Неизвестный токен"; // Проверка на undefined
            //     let current = document.getElementById("current"); 
            //     current.innerText = `Текущая цена ${time_name}:`;
            //     current.style.color = latest_price > previous_price ? "green" : "red";
            // } else {
            //     console.error("❌ Ошибка: массив price_list пуст или не содержит данных!");
            // }


            for (let elem of data.price_list) {
                let row = table.insertRow(-1);  // Добавляем новую строку
                row.insertCell(0).innerText = elem.timestamp;  // Время

                /*let priceCell = row.insertCell(1)
                if (elem.diff > 0) priceCell.innerText = elem.price + " ▲";  // Цена
                else if (elem.diff < 0) priceCell.innerText = elem.price + " 🔽";
                else priceCell.innerText = elem.price*/
                let priceCell = row.insertCell(1)
                priceCell.innerHTML = elem.price + "  " + elem.direction;  // Цена + стрелка (HTML)
                //row.insertCell(2).innerText = elem.diff !== null ? elem.diff : "-";  // Разница // тернарный оператор {% endcomment %}
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
                /*for(let item of document.querySelectorAll('td');)
                    /*if(item == diff.innerText) > 0){ elem.diff.style.color = 'green';} 
                    else if (Number(elem.diff.innerText) < 0)  {elem.diff.style.color = 'red';}
                    else {elem.diff.style.color = 'black';} */
            }
            updatechartInstance(data)
            currentAllPrice(latestData)
        })
        .catch(error => console.error('Ошибка загрузки данных:', error))
}

// setInterval(fetchData, 60000);  // 🔄 Обновляем цену каждые 5 секунд
// fetchData(timeSymbol)  // 🔥 Запускаем сразу при загрузке страницы

// let lab = ""
// let chartInstance = null ;     // Глобальная переменная для хранения графика
// function updatechartInstance(getData) {
//     console.log(`chartInstancetimeSymbol = ${timeSymbol}`)
//     // console.log(`chartInstance_time_name = ${time_name}`)
//     let time_name = getData.price_list[0].name
//     // lab = chartInstance.data.datasets[0].label

//     //✅ Если график уже есть, уничтожаем его перед созданием нового
//     if (chartInstance !== null) {
//         chartInstance.destroy();
//         console.log("🛑 Старый график удалён!");
//     }

//     // let time_name = getData.price_list[0].name 
//     const ctx = document.getElementById('chartInstance').getContext('2d');
//     // console.log("✅ WebSocket доступен, используем его.");
//     chartInstance = new Chart(ctx, {
//         type: 'line',
//         data: {
//             labels: [],
//             datasets: [{
//                 label: `${time_name} Price (USD)`,
//                 data: [],
//                 borderColor: "gray",  // Базовый цвет линии
//                 backgroundColor: "rgba(0, 0, 255, 0.1)",
//                 borderWidth: 2, // Базовая толщина
//                 fill: true,
//                 pointRadius: 3, // Радиус точек
//                 pointBackgroundColor: "gray", // Цвет точек
//                 segment: {
//                     borderColor: ctx => {
//                         const chart = ctx.chart;
//                         const { data } = chart.data.datasets[0];
//                         const index = ctx.p1DataIndex;  // Индекс текущей точки

//                         // Если нет предыдущей точки, оставляем серый цвет
//                         if (index === 0) return "gray";

//                         // Меняем цвет линии в зависимости от направления
//                         return data[index] > data[index - 1] ? "green" : "red";
//                     },
//                     borderWidth: ctx => {
//                         const chart = ctx.chart;
//                         const { data } = chart.data.datasets[0];
//                         const index = ctx.p1DataIndex;

//                         // Если нет предыдущей точки, оставляем стандартную толщину
//                         if (index === 0) return 2;

//                         // Толстая линия при росте, тонкая при падении
//                         return data[index] < data[index - 1] ? 7 : 1;
//                     }
//                 }
//             }]
//         },
//         options: {
//             scales: {
//                 x: { title: { display: true, text: "Время" } },
//                 y: { title: { display: true, text: "Цена (USD)" } }
//             }
//         }
//     });

//     // chartInstance.data.datasets[0].label = `${time_name} Price (USD)`
//     if (typeof window.time_name === 'undefined') {
//         console.warn(`${time_name} не найден в window.`);
//     } else {
//         console.warn(`${time_name}уже определён (например, MetaMask). Конфликт устранён.`);
//     }
//     // time_name = getData.price_list[0].name;
//     // console.log(`chartInstance_time_name = ${time_name}`)
//     // ✅ Подключаем WebSocket
//     // const socket = new WebSocket("ws://127.0.0.1:8000/ws/eth-price/");
//     // const socket = new WebSocket(
//     //     window.location.protocol === "https:" ? 
//     //     `wss://${window.location.host}/ws/eth-price/` : 
//     //     `ws://${window.location.host}/ws/eth-price/`
//     // );
//     // socket.onmessage = function (event) {
//     //     console.log("📩 Данные от WebSocket:", event.data);
//     //     const data = JSON.parse(event.data);

//     // socket.onmessage = function (event) {
//     //     console.log("📩 Данные от WebSocket:", event.data);
//     //     const data = JSON.parse(event.data);
//     //     if (!data.prices || !Array.isArray(data.prices)) {
//     //         console.error("❌ Ошибка: Данные WebSocket отсутствуют или имеют неверный формат.");
//     //         return;
//     //     }
//     // ✅ 1. Разворачиваем массив, чтобы новые данные были в конце
//     const sortedPrices = getData.price_list;
//     console.log(getData.price_list[0].name, getData.price_list[0].price)
//     // const sortedPrices = data.prices;
//     // ✅ 2. Перебираем весь массив и обновляем график
//     chartInstance.data.labels = [];
//     chartInstance.data.datasets[0].data = [];
//     //ethChart.data.datasets[0].borderColor = [];
//     sortedPrices.forEach(priceData => {
//         // if(i < length.sortedPrices-1) {           // ⬅️ Проверяем, чтобы не выйти за границы массива
//         //     if(sortedPrices[i].price > sortedPrices[i+1].price) ethChart.data.datasets[0].backgroundColor.unshift("green")
//         //     else ethChart.data.datasets[0].backgroundColor.unshift("red")
//         /*sortedPrices[i].price > sortedPrices[i+1].price? 
//         ethChart.data.datasets[0].borderColor="red":
//         ethChart.data.datasets[0].borderColor="green";*/

//         chartInstance.data.labels.unshift(priceData.timestamp);
//         chartInstance.data.datasets[0].data.unshift(priceData.price);
//     });
//     // красим сегменты(звенья) графика и фон под ними
//     chartInstance.data.datasets[0].segment = {
//         borderColor: ctx => {
//             const index = ctx.p1DataIndex; // Индекс второй точки сегмента
//             if (!index || index === 0) return "gray"; // Первая точка — серая
//             return chartInstance.data.datasets[0].data[index] > chartInstance.data.datasets[0].data[index - 1]
//                 ? "green"  // 📈 Если цена растёт — зелёный
//                 : "red";    // 📉 Если падает — красный
//         },
//         backgroundColor: ctx => {
//             const index = ctx.p1DataIndex;
//             if (!index || index === 0) return "rgba(128, 128, 128, 0.1)"; // Серый, если первая точка
//             return chartInstance.data.datasets[0].data[index] > chartInstance.data.datasets[0].data[index - 1]
//                 ? "rgba(0, 255, 0, 0.1)"  // 📈 Зелёная прозрачность
//                 : "rgba(255, 0, 0, 0.1)";  // 📉 Красная прозрачность
//         }
//     };
//     // цвет межзвеньевой точки
//     chartInstance.data.datasets[0].borderColor = sortedPrices.reverse().map((priceData, i) => {
//         if (i === 0) return "gray";
//         return sortedPrices[i].price > sortedPrices[i - 1].price ? "green" : "red";
//     });
//     // размер межзвеньевой точки
//     chartInstance.data.datasets[0].borderWidth = sortedPrices.map((priceData, i) => {
//         if (i === 0) return 2;
//         return sortedPrices[i].price > sortedPrices[i - 1].price ? 4 : 4;
//     });

//     // ethChart.data.datasets[0].borderColor = borderColors;
//     /* ✅ 3. Ограничиваем до 10 точек (чтобы не перегружать график)
//     while (ethChart.data.labels.length > 10) {
//         ethChart.data.labels.shift();
//         ethChart.data.datasets[0].data.shift();
//     } */

//     // ✅ 4. Обновляем график
//     chartInstance.update();
// }

// socket.onclose = function(event) {
//     console.log("WebSocket закрыт, код:", event.code);
// };

let chartInstance = null;  // Храним текущий график

function updatechartInstance(getData) {
    console.log(`chartInstancetimeSymbol = ${tokenSymbol}`)
    const token_name = getData.price_list[0].name;
    console.log(`chartInstance_time_name = ${token_name}`)

    const ctx = document.getElementById('tokenChart').getContext('2d');
    // console.log(`ctx = ${document.getElementById('chartInstance')}`)

    const labels = getData.price_list.reverse().map(entry => entry.timestamp.replace('20', ""));  // Метки оси X (время)
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
                    pointRadius: 3, // Радиус точек
                    // pointBackgroundColor: "white", // Цвет точек
                    // pointBorderColor: "blue",
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
                // datasets: [{
                //     label: `${token_name} Price (USD)`,
                //     data: prices,
                //     borderColor: "blue",  
                //     backgroundColor: "rgba(0, 0, 255, 0.1)",  
                //     tension: 0.3  // ✅ Делаем линии плавными
                // }]
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

// 🔥 Что улучшено?
// ✅ Больше нет destroy(), вместо этого просто обновляем данные.
// ✅ Добавлена анимация duration: 1000 и easing: 'easeInOutQuad' (гладкое обновление).
// ✅ Используется tension: 0.3, чтобы линии были плавнее.
// ✅ Добавлено autoSkip и maxTicksLimit, чтобы ось X выглядела аккуратно.

// Теперь график перерисовывается красиво и плавно, без грубых скачков! 🚀📊✨


function currentAllPrice(latestData) {
    /* функциия для отображения текущей цены для каждого такена*/
    console.log(`latestData=${latestData}`)

    let allPrice = document.getElementById("all-price");
    let allPriceParag = allPrice.getElementsByTagName("p");
    console.log(`len allPriceParag=${allPriceParag.length}`)
    console.log(`len latestData=${latestData.length}`)
    // latestData.forEach(priceName => {
    //     if (allPrice) {
    //         allPrice.innerText = `${priceName.name} ${priceName.price}`
    //     } else {
    //         console.error("❌ Ошибка: allPrice & latestData  не найдены!");
    //     }
    // })

    for (let i = 0; i < allPriceParag.length; i++) {
        for (let j = 0; j < latestData.length; j++) {
            if (i === j) {
                allPriceParag[i].innerText = latestData[j].dif > 0 ?`${latestData[j].name} ${latestData[j].price}↑`:`${latestData[j].name} ${latestData[j].price}↓`
                allPriceParag[i].style.color = latestData[j].dif > 0  ? "green" : "red";
                // priceElement.innerText = latest_price + " USD " + (latest_price > previous_price ? "↑" : "↓");
            }
        }
    }
    // allPriceParag.forEach((item, i) => {
    //     allPriceParag.forEach((elem, j) => {
    //         if (i === j) {
    //             allPriceParag[i].innerText = `${latestData[j].name} ${latestData[j].price}`
    //         }
    //     })

        
    // })
}
// function div2ParaElems() {
//     const div2 = document.getElementById("div2");
//     const div2Paras = div2.getElementsByTagName("p");
//     const num = div2Paras.length;
//     alert(`There are ${num} paragraph in #div2`);
//   }



