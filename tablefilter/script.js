const typeToFuncMap = {
    "text": "textComp",
    "number": "numericalComp",
    "date": "dateComp"
};


function search(inputId, tableId, targetIdx, searchComp) {
    let input = document.getElementById(inputId);
    let filter = input.value.toUpperCase();

    let table = document.getElementById(tableId);
    let trs = table.getElementsByTagName('tr');

    // do the search
    [...trs].slice(2).forEach(tr => {
        td = tr.getElementsByTagName("td")[targetIdx];
        let value = td.textContent || td.innerText;
        tr.style.display = searchComp(value, filter) ? "" : "none";
    });
}


/**
 * Returns if the given filter is inside the value string
 * 
 * @param {String} value: the value to apply the filter
 * @param {String} filter: the filter to apply
 * 
 * @return {Boolean} if the filter is inside the value
 */
function textComp(value, filter) {
    return (value) && (value.toUpperCase().indexOf(filter) > -1);
}


/**
 * Performs a numerical comparison between the given value and
 * the filter. If the filter has no mathematical operations (<, >, =, >=, <=)
 * then textComp is called
 * 
 * @param {String | Number} value: the value to apply the filter
 * @param {String} filter: the filter to apply. The filter string must be in the form
 *      "{mathOp}{Value}" where "mathOp" is (<, >, =, >=, <=) and "Value" is a numerical
 *      value (1, 2, 3.14, ...). If no "mathOp" is given then a textComp is performed
 * 
 * @return {Boolean} if the mathematical equation holds
 */
function numericalComp(value, _filter) {
    // remove white spaces
    let filter = _filter.replace(/\s+/g, '');
    let compOp = filter[0]; // >, <, =

    switch (compOp) {
        case "<":
            return filter[1] == "=" ? 
                Number(value) <= Number(filter.slice(2)) : 
                Number(value) < Number(filter.slice(1));
        case ">":
            return filter[1] == "=" ? 
                Number(value) >= Number(filter.slice(2)) : 
                Number(value) > Number(filter.slice(1));
        case "=":
            return value == filter.slice(1);
        default:
            return textComp(value, filter); 
    }
}


/**
 * Performs a date comparison between the given value and
 * the filter. The date is transformed into a number (time value in ms)
 * and calls numericalComp using the converted dates
 * 
 * @param {String} value: the date string to apply the filter
 * @param {String} filter: the filter to apply. The filter string must be in the form
 *      "{mathOp}{Value}" where "mathOp" is (<, >, =, >=, <=) and "Value" is a date
 *      value ("2012-02-12", "2015/05/24", "2022 05 25", ...). If no "mathOp" 
 *      is given then a textComp is performed
 * 
 * @return {Boolean} if the mathematical equation holds
 */
function dateComp(_value, filter) {
    if (!filter) return textComp(_value, "");

    
    let value = new Date(_value);
    value = String(value.getTime());

    let datefilter = "";
    if (["<", ">", "="].includes(filter[0]))
        datefilter += filter[0];
    
    let startIdx = 1;
    if (filter[1] == "=") {
        datefilter += filter[1];
        startIdx++;
    }

    // ignore white spaces between date and compOp
    while (filter[startIdx] == " ") {
        startIdx++;
    }

    console.log(filter.slice(startIdx));
    let date = new Date(filter.slice(startIdx));
    datefilter += String(date.getTime());

    console.log("filter", datefilter);
    console.log("value", value);
    return numericalComp(value, datefilter);
}


// sorting
const getCellValue = (tr, idx) => tr.children[idx].innerText || tr.children[idx].textContent;

const comparer = (idx, asc) => (a, b) => ((v1, v2) =>
    v1 !== '' && v2 !== '' && !isNaN(v1) && !isNaN(v2) ? v1 - v2 : v1.toString().localeCompare(v2)
)(getCellValue(asc ? a : b, idx), getCellValue(asc ? b : a, idx));



function addTableSearch(tableId, config={}) {
    const table = document.getElementById(tableId);
    let ths = table.getElementsByTagName('th');

    let row = table.insertRow(1);
    for (let i = 0; i < ths.length; i++) {
        let thName = ths[i].innerText;
        let cell = row.insertCell(i);

        let funcName = "textComp";
        if (config.hasOwnProperty("type") && (
            config.type.hasOwnProperty(i) || config.type.hasOwnProperty(thName)) ) { 
                funcName = typeToFuncMap[config.type[i] || config.type[thName]];
        }
        cell.innerHTML = `<input type="text" id="myInput${i}" 
            onkeyup="search('myInput${i}', '${tableId}', ${i}, ${funcName})"
            placeholder="Search"
            style="width: 80%">`;
    }

    table.querySelectorAll('th').forEach(th => th.addEventListener('click', (() => {
        const table = th.closest('table');
        Array.from(table.querySelectorAll('tr:nth-child(n+2)'))
            .sort(comparer(Array.from(th.parentNode.children).indexOf(th), this.asc = !this.asc))
            .forEach(tr => table.appendChild(tr));
    })));
}