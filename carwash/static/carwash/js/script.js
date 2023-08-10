/* функция отключения выбора услуг входящих в choice1 и choice2 */
function WashDis(el, t) {
    WashEn()
    if(document.getElementById("id_service_"+el).checked) {
        for(let i=5;i <= t; ++i) {
            document.getElementById("id_service_"+i).checked = false;
            document.getElementById("id_service_"+i).disabled = true;
        }
    }

    /* имитируем поведение RadioButtun "первых четырех услуг"- отключаем другие кнопки кроме выбранной */
    for(let i=1; i < 5; ++i) {
        if(i!=el) document.getElementById("id_service_"+i).checked = false;
    }
    Calculate() /* Считаем общее время работ и отображаем подходящие времена */
}

/* функция обратного включения услуг не входящих в choice3 и choice4 */
function WashEn() {
    for(let i=5;i <= 9; ++i) {
        document.getElementById("id_service_"+i).disabled = false;
    }
}

function WashEngine(el) {
    /* имитируем поведение RadioButtun "мойка двигателя" - отключаем другие кнопки кроме выбранной */
    for(let i=16; i < 18; ++i) {
        if(i!=el) document.getElementById("id_service_"+i).checked = false;
    }
    Calculate() /* Считаем общее время работ и отображаем подходящие времена */
}

/* Проверка что выбраны хотя бы 1 услуга и время, иначе кнопка записаться - неактивна */
function CheckChoice() {
    let list_services = document.querySelectorAll("div.services-choice > table > tbody > tr > td > input"); /* получаем список всех choice-input */
    let list_times = document.querySelectorAll("div.day-content > input"); /* список всех времен */

    function CheckList(iterable_list) {
        for (let item of iterable_list) {
            if (item.checked) {
                return true;
            }
        }
        return false;
    }

    if(CheckList(list_services) && CheckList(list_times)) document.getElementById("registration").disabled = false;
    else document.getElementById("registration").disabled = true;
}

/* функция подсчёта общего времени для работ с авто и отображение подходящих времён */
function Calculate() {
    
    let list_services = document.querySelectorAll("div.services-choice > table > tbody > tr > td > input"); /* получаем список всех choice-input */
    let overal_time = 0; /* общее время работ с автомобилем */
    let flag = true;  /* флаг для определения выбраны ли уже услуги 7,8,9 */

    /* подсчёт общего времени выбранных услуг / если больше одной услуги из диапазона 7-9, то время берётся только за одну услугу */
    list_services.forEach(item => {
        if(item.checked) {
            if(["id_service_7", "id_service_8", "id_service_9"].includes(item.id)) {
                if(flag) {
                    overal_time += Number(item.dataset.processTime);
                    flag = false
                }
            }
            else {
                overal_time += Number(item.dataset.processTime);
            }
        }
    });

    /* Определяем свободные времена */
    let dict_div = document.querySelectorAll("div.day-content > input"); /* список всех времен */

    /* Каждый раз включаем все кнокпки времён которые выключились от выбора услуг */
    for(let h of dict_div) {
        if(h.name != "dis") {
            h.disabled = false;
        }
    }

    let list_input = []; /* временный список объектов input(время) */
    let res_dict = {}; /* словарь объектов input(время) и их доступного времени */
    
    for(let i of dict_div) list_input.push(i); /* создаем временный список времен*/

    let quantitytimes = list_input.length; /* кол-во времен (66) */
    
    for(let c=0; c < quantitytimes; ++c) {
        let time = list_input.shift();  /* забираем первый элемент из списка */
        let period = 30;                /* начально доступный период у текущего времени */

        if(time.name=='dis') {             /* если время отключено то его период равен 0мин */
            res_dict[c] = [time, 0];
            continue;
        }
        
        if(time.value.includes("20:30")) {  /* усли время равно "20:30" то его период 30 мин до конца */
            res_dict[c] = [time, 30];
            continue;
        }
        
        for(let k of list_input) {
            if(k.name=='dis') {                   /* если текущее время выключено, то обрабатываемое время получает период */
                res_dict[c] = [time, period];
                break;
            }

            if(k.value.includes("20:30")) {
                period = period + 30;
                res_dict[c] = [time, period];
                break;
            }
            period = period + 30;
        } 
    }

    /* Выключаем кнопки времён которые не подходят под общее время услуг */
    for(let k in res_dict) {
//        console.log(k, res_dict[k], overal_time);
        let [r, g] = res_dict[k];
        if(g < overal_time) {
            r.checked = false;
            r.disabled = true;
        }
    }
    console.log(overal_time)
    CheckChoice()   /* Включаем или отключаем кнопку записи */
    TotalCost(list_services, overal_time)

}

function TotalCost(list_services, overal_time) {
    let total_cost = 0;

    list_services.forEach(item => {
        if(item.checked) {
            console.log(item.dataset.price)
            total_cost += Number(item.dataset.price);
        }
    });
    let div = document.getElementById("comm")
    let ct = div.dataset.carType

    document.getElementById("overal-time").innerHTML = "Общее время работ: " + overal_time + " мин.";
    document.getElementById("total-cost").innerHTML = "Общая стоимость услуг: " + total_cost + " р.";
}

