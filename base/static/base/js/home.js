// Funções auxiliares
function getBusinessDatesCount(startDate, endDate) {
    let count = 0;
    const curDate = new Date(startDate.getTime());
    while (curDate <= endDate) {
        if (curDate.getDay() !== 0 && curDate.getDay() !== 6) count++;
        curDate.setDate(curDate.getDate() + 1);
    }
    return count;
}
function lastBussinessDay(date) {
    if (date.getDay() > 0 && date.getDay() < 6 && getBusinessDatesCount(date, new Date()) >= 6) return date;
    date.setTime(date.getTime() - 86400000);
    return lastBussinessDay(date);
}
const zeroPadLeft = (num, places) => String(num).padStart(places, "0");
const formatDate = (date) => date.getFullYear() + "-" + zeroPadLeft(date.getMonth() + 1, 2) + "-" + date.getDate();
const getCookieValue = (name) => document.cookie.match("(^|;)\\s*" + name + "\\s*=\\s*([^;]+)")?.pop() || "";
const setCookieValue = (name, value) => (document.cookie = name + "=" + value + ";");

// Contruir o gráfico
function buildChart() {
    $("#moedaBase").attr('disabled', true);
    $("#moeda").attr('disabled', true);
    $("#dataInicial").attr('disabled', true);
    $("#dataFinal").attr('disabled', true);
    $("#carregando").html('Carregando...');
    moedaBase = $("#moedaBase option:selected").val();
    moeda = $("#moeda option:selected").val();
    moedaSimbolo = $("#moeda option:selected").text().split(" - ")[1];
    $("#title").html("Cotação " + moedaBase + "/" + moeda);
    $.get({
        url: "/api/grafico/" + moedaBase + "/" + moeda + "/?format=json&dataInicial=" + $("#dataInicial").val() + "&dataFinal=" + $("#dataFinal").val(),
        success: function (data) {
            $("#moedaBase").attr('disabled', false);
            $("#moeda").attr('disabled', false);
            $("#dataInicial").attr('disabled', false);
            $("#dataFinal").attr('disabled', false);
            $("#carregando").html('');
            Highcharts.chart("highcharts", {
                chart: {
                    zoomType: "x",
                },
                title: {
                    text: "Câmbio " + moeda + " para " + moedaBase + " nos últimos dias",
                },
                subtitle: {
                    text: document.ontouchstart === undefined ? "Clique e arraste o mouse para dar zoom" : "Pinch the chart to zoom in",
                },
                xAxis: {
                    type: "datetime",
                },
                yAxis: {
                    title: {
                        text: "Câmbio " + moedaSimbolo,
                    },
                },
                legend: {
                    enabled: false,
                },
                plotOptions: {
                    area: {
                        fillColor: {
                            linearGradient: {
                                x1: 0,
                                y1: 0,
                                x2: 0,
                                y2: 1,
                            },
                            stops: [
                                [0, Highcharts.getOptions().colors[0]],
                                [1, Highcharts.color(Highcharts.getOptions().colors[0]).setOpacity(0).get("rgba")],
                            ],
                        },
                        marker: {
                            radius: 2,
                        },
                        lineWidth: 1,
                        states: {
                            hover: {
                                lineWidth: 1,
                            },
                        },
                        threshold: null,
                    },
                },

                series: [
                    {
                        type: "area",
                        name: moeda + " para " + moedaBase,
                        data: data,
                    },
                ],
            });
        },
    });
}

// Atualizar o gráfico quando houver uma mudança nos parâmetros
$("#moedaBase").change((event) => {
    buildChart();
    // salvar preferência de moeda nos cookies
    setCookieValue("moedaBase", $("#moedaBase").val());
});
$("#moeda").change((event) => {
    buildChart();
    // salvar preferência de moeda nos cookies
    setCookieValue("moeda", $("#moeda").val());
});
$("#dataInicial").change((event) => {
    // Verificar a validade da data
    if (event.target.value > $('#dataFinal').val()) {
        // Se a data é inválida, avisa o usuário e seta a data padrão do campo
        alert('A data inicial não pode ser maior que a data final!');
        today = new Date();
        today.setTime(today.getTime() - 5 * 86400000);
        dataInicial = lastBussinessDay(today);
        $("#dataInicial").val(formatDate(dataInicial));
        return buildChart();
    }
    return buildChart();
});
$("#dataFinal").change((event) => {
    // Verificar a validade da data
    if (event.target.value < $('#dataInicial').val()) {
        // Se a data é inválida, avisa o usuário e seta a data padrão do campo
        alert('A data final não pode ser menor que a data inicial!');
        today = new Date();
        $("#dataFinal").val(formatDate(today));
        return buildChart();
    }
    return buildChart();
});

$(document).ready(() => {
    // Setar data final (dia de hoje)
    today = new Date();
    $("#dataFinal").val(formatDate(today));

    // Setar data inicial (5 dias úteis atrás)
    today.setTime(today.getTime() - 5 * 86400000);
    dataInicial = lastBussinessDay(today);
    $("#dataInicial").val(formatDate(dataInicial));

    // Ler valores preferenciais de moedas nos cookies
    moedaBase = getCookieValue("moedaBase");
    moeda = getCookieValue("moeda");

    // Setar valores das moedas
    $("#moedaBase").val(moedaBase ? moedaBase : "USD");
    $("#moeda").val(moeda ? moeda : "BRL");

    // Contruir o gráfico
    buildChart();
});
