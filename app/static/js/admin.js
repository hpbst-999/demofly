const searchInput = document.getElementById("search-input");
const searchBtn = document.getElementById("btn-search");
let currentTable = null; // текущая выбранная таблица
let selectedRowData = null; // выбранная строка

document.addEventListener("DOMContentLoaded", function () {
    const sidebarLi = document.querySelectorAll(".sidebar-li");

    sidebarLi.forEach(li => {
        li.onclick = function () {
                    document.querySelectorAll("#sidebar-tables li").forEach(el => {
                        el.classList.remove("active");
                    });
                    li.classList.add("active");
                    const currentTable = li.innerHTML;
                    console.log("Выбрана таблица:",currentTable);
                    
                };
    });
});