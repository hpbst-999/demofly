const searchInput = document.getElementById("search-input");
const searchBtn = document.getElementById("btn-search");
let currentTable = null; // текущая выбранная таблица
let currentList = null;  // List.js объект
let selectedRowData = null; // выбранная строка

document.addEventListener("DOMContentLoaded", function () {
    fetch("/api/admin/entity")
        .then(response => response.json())
        .then(data => {
            const sidebar = document.getElementById("sidebar-tables");
            sidebar.innerHTML = "";
            searchInput.innerHTML = "";
            data.tables.forEach(table => {
                const li = document.createElement("li");
                li.className = "list-group-item list-group-item-action";
                li.textContent = table.name;

                li.onclick = function () {
                    document.querySelectorAll("#sidebar-tables li").forEach(el => {
                        el.classList.remove("active");
                    });
                    li.classList.add("active");
                    console.log("Выбрана таблица:", table.name);
                    loadMainTable(table.name);
                };

                sidebar.appendChild(li);
            });
        })
        .catch(error => console.error("Ошибка загрузки таблиц:", error));
});

searchBtn.addEventListener("click", function () {
    if (!currentTable) return;
    const query = searchInput.value.trim();
    loadMainTable(currentTable, query);
});


function loadMainTable(tableName, searchQuery = "") {
    const mainTable = document.getElementById("main-table");
    mainTable.innerHTML = "Загрузка данных...";

    currentTable = tableName;
    currentList = null; // сбрасываем прошлый List.js объект

    mainTable.classList.remove("small-font");
    mainTable.classList.remove("small-font2");
    if (tableName === "routes") mainTable.classList.add("small-font");
    if (tableName === "flights") mainTable.classList.add("small-font2");

    let url = "/api/admin/search?t=" + tableName;
    if (searchQuery) url += "&q=" + encodeURIComponent(searchQuery);

    fetch(url)
        .then(resp => resp.json())
        .then(result => {
            if (result.error) {
                mainTable.innerHTML = "Ошибка: " + result.error;
                return;
            }

            const rows = result.data;
            if (!rows || rows.length === 0) {
                mainTable.innerHTML = "<p>Данных нет</p>";
                return;
            }

            const columns = Object.keys(rows[0]);

            // создаём контейнер для List.js
            mainTable.innerHTML = `
                
                <table class="table table-striped table-bordered table-hover">
                    <thead>
                        <tr>
                            ${columns.map(col => `<th class="sort" data-sort="${col}">${col}</th>`).join('')}
                        </tr>
                    </thead>
                    <tbody class="list"></tbody>
                </table>
            `;

            const tbody = mainTable.querySelector("tbody");

            // добавляем строки
            rows.forEach(row => {
                const tr = document.createElement("tr");
                tr.classList.add("clickable-row");
                tr.onclick = function () 
                {
                    const allRows = mainTable.querySelectorAll("tbody tr");
                    allRows.forEach(r => r.classList.remove("table-act"));
                    tr.classList.add("table-act");
                    selectedRowData = row;
                };
                columns.forEach(col => {
                    const td = document.createElement("td");
                    td.classList.add(col); // нужно для List.js
                    td.textContent = row[col] !== null ? row[col] : "";
                    tr.appendChild(td);
                });
                tbody.appendChild(tr);
            });

            // инициализация List.js
            currentList = new List(mainTable.id, {
                valueNames: columns,
                listClass: 'list',
                sortClass: 'sort'
            });

        })
        .catch(err => {
            mainTable.innerHTML = "Ошибка загрузки таблицы";
            console.error(err);
        });
}




const deleteBtn = document.getElementById("btn-delete");

deleteBtn.addEventListener("click", function () {
    if (!selectedRowData || !currentTable) {
        Swal.fire({
            title: "Ошибка",
            text: "Сначала выберите строку в таблице!",
            icon: "info",
            confirmButtonColor: "#0d6efd"
        });
        return;
    }

    Swal.fire({
        title: "Вы уверены?",
        text: "Эта запись будет удалена!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Да, удалить",
        cancelButtonText: "Отменить"
    }).then((result) => {
        if (result.isConfirmed) {
            fetch("/api/admin/delete", {
                method: "DELETE",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    table: currentTable,
                    row: selectedRowData 
                })
            })
            .then(response => response.json()) 
            .then(data => {
                if (data.success) {
                    Swal.fire({
                        title: "Успешно!",
                        text: data.message || "Запись удалена.",
                        icon: "success"
                    });
                    loadMainTable(currentTable, searchInput.value.trim());
                    selectedRowData = null;
                } else {
                    Swal.fire("Ошибка", data.error || "Не удалось удалить", "error");
                }
            })
            .catch(err => {
                console.error(err);
                Swal.fire("Ошибка", "Проблема с сетью или сервером", "error");
            });
        }
    });
});
const editBtn = document.getElementById("btn-edit");

editBtn.addEventListener("click", function() {
    if (!selectedRowData) {
        Swal.fire({
            icon: 'info',
            title: 'Стоп!',
            text: 'Сначала выберите строку в таблице, кликнув по ней.',
            confirmButtonColor: '#0d6efd' 
        });
        return;
    }
});