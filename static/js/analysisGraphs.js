//This global variable is used to hold the handle for all the charts created so that they can be resized on tab changes
//This holds objects with keys:
//chart - holds the actual chart handle
//type - holds the kind of graph it is. Seasonal Decomp must be called SD
var charts = []

function getData(header) {
    
    //=========VERY IMPORTANT NOTE=================
    //Javascript DOES NOT pass copies into functions. So, if youo put any of these arrays into a graphing function and need to alter the data in any way (i.e. padding with NaNs) you MUST make a copy of the array in the function and make changes ONLY to the copy of that array. calling <arrayname>.slice() will make an exact copy of <arrayname> and any changes you make to that copy will not affect these arrays
    
    //get selected headers
    var selectedHeader;
    if(header=="NULL") {
        selectedHeader = document.getElementById("headers").getElementsByTagName("li")[0].id;
    } else {
        selectedHeader = header;
    }
    console.log(selectedHeader)
    //parse the json string from server and get the data from the header we want
    results = JSON.parse(resultJSON);
    data = results[selectedHeader]
    
    //push data from the selected header into all the arrays needed to visualize
    var actualDate = []
    var futureDate = []
    var actual = ["Actual"]
    var predicted = ["Predicted"]
    var forecasted = ["Forecasted"]
    var SDTrend = ["SDTrend"]
    var SDSeasonal = ["SDSeasonal"]
    var SDResidual = ["SDResidual"]
    
    actualDate.push.apply(actualDate, data.actualTime)
    
    futureDate.push.apply(futureDate, data.actualTime)
    futureDate.push.apply(futureDate, data.futureTime)
    
    actual.push.apply(actual, data.actualValues)
    
    forecasted.push.apply(forecasted, data.forecastedValues)
    
    predicted.push.apply(predicted, data.predictedValues)
    
    SDTrend.push.apply(SDTrend, data.SDTrend)
    
    SDSeasonal.push.apply(SDSeasonal, data.SDSeasonal)
    
    SDResidual.push.apply(SDResidual, data.SDResidual);
    
    createForecastedGraph(actual, forecasted, futureDate)
    createPvAGraph(actual, predicted, actualDate)
    createSeasonalDecompGraph(actual, SDTrend, SDSeasonal, SDResidual, actualDate)
    createResidualGraph(actual, predicted, actualDate)
    
    //when you press the generate graph button, you should be brought to the forecasted tab, so we need to pass the forecasted tab and the forecasted container to this function
    toggleShownGraph(document.getElementById("forecastedTab"), document.getElementById("forecastedContainer"))
}

/*toggleShownGraph: highlights the selected graph tab and displays only the graph related to that tab
Input: Element - the html dom element of the tab selected
Input: graphContainer - the html dom element of the container of the graph that needs to be displayed
*/
function toggleShownGraph(element, graphContainer) {
    //grab the navbar from the dom
    tabNav = document.getElementById("tabNav")
    //get the children (the <li> elements)
    childrenLi = tabNav.children
    tabs = []
    //get the <a> tags from the <li> tabs
    for(var i = 0; i < childrenLi.length; i++) {
        a = childrenLi[i].children
        tabs.push(a)
    }
    //clear class of each <a> tag to make it look unselected
    for(var i = 0; i < tabs.length; i++){
        tabs[i][0].removeAttribute("class")
    }
    //make the selected <a> tag look selected
    element.setAttribute("class", "activeTab")
    //this holds the container dom elements of all the graphs
    containers = [document.getElementById("forecastedContainer"), document.getElementById("pvaContainer"), document.getElementById("sdContainer"), document.getElementById("residualContainer")]
    //hide all graphs
    for(var i = 0; i < containers.length; i++) {
        containers[i].style.display = "none"
    }
    //show only the graph we want to see
    graphContainer.style.display = "block"
    //resize all graphs on tab switch
    for (var i = 0; i < charts.length; i++) {
        charts[i].chart.resize()
    }
    
}

function createForecastedGraph(actual, forecasted, futureDate) {
    //in order to get the forecasted graph to start plotting after
    //the actual values graph, we need to pad it with NaNs
    
    //this variable holds the forecasted values with padded NaNs
    var graphableForecasted = ["Forecasted"]
    
    //we stop 2 short of the length of the actual values array
    //1) To ignore the initial value of "Actual" in the array
    //2) To ignore the last value of the actual array, which we will push into the graphableForecasted array
    for (var i = 0; i < actual.length - 2; i++)
        graphableForecasted.push(NaN)
        
    //here we add the last value of the actual values array so that there is a line drawn between the last point of the actual value line and the first point of the forecasted value line    
    graphableForecasted.push(actual.slice(-1)[0])
    
    //this line adds the values of the forecasted array to the graphableForecasted array. Forecasted.slice(1) is used to remove the "Forecasted" string that is the first element of the forecasted array
    graphableForecasted.push.apply(graphableForecasted, forecasted.slice(1))
    
    //Since javascript does not pass copies into functions, we need to make a graphableActual variable so we can alter the contents of the actual array without making permanent changes
    graphableActual = ["Actual"]
    
    //here we add the values of the actual array to graphableActual (again skipping the first string element using slice(1))
    graphableActual.push.apply(graphableActual, actual.slice(1))
    
    //here we pad the end of the graphableActual array with NaNs so the tooltip shows up for all values of the graph
    for (var i = 0; i < forecasted.length - 1; i++)
        graphableActual.push(NaN)
        
    var chart = c3.generate({
        bindto: '#Forecasted',
        data: {
            //make sure that graphableForecasted is plotted first so that it doesnt look like there is an extra forecasted point that is really the last actual value point
            columns: [
                graphableForecasted, graphableActual
            ],
            colors: {
                Actual: "#29AFDF",
                Forecasted : "#ED2835"
            }
        },
        subchart: {
            show: true
        },
        axis: {
            x: {
                type: 'categories',
                categories: futureDate,
                tick: {
                    multiline: false,
                    culling: {
                        max: 15
                    }
                },
                label: {
                text: 'Time Series',
                position: 'outer-center'
                }
            },
            y: {
                label: {
                    text: "Values",
                    position: 'outer-middle'

                }
            }
        },
        zoom: {
            enabled: true,
            rescale: true
        },
        legend: {
            position: 'right'
        }
    });
    //MAKE SURE YOU DO THIS LINE FOR ALL CHARTS. YOU MUST CHANGE THE 'type' KEY TO THE TYPE OF GRAPH YOU ARE USING
    charts.push({'chart': chart, 'type': "Forecasted"})
}
    
function createPvAGraph(actual, predicted, actualDate) {
    var chart = c3.generate({
        bindto: '#PvA',
        data: {
            columns: [
               actual, predicted
            ],
             colors: {
                Actual: "#29AFDF",
                Predicted : "#ED2835"
            }
        },
        subchart: {
            show: true
        },
        axis: {
            x: {
                type: 'category',
                categories: actualDate,
                tick: {
                    multiline: false,
                    culling: {
                        max: 15
                    }
                },
                label: {
                text: 'Time Series',
                position: 'outer-center'
                }
            },
            y: {
                label: {
                    text: "Values",
                    position: 'outer-middle'

                }
            }
        },
        zoom: {
            enabled: true,
            rescale: true
        },
        legend: {
            position: 'right'
        }
    });
    //MAKE SURE YOU DO THIS LINE FOR ALL CHARTS. YOU MUST CHANGE THE 'type' KEY TO THE TYPE OF GRAPH YOU ARE USING
    charts.push({'chart': chart, 'type': "PvA"})
}

function createSeasonalDecompGraph(actual, SDTrend, SDSeasonal, SDResidual, actualDate) {
    var chart1 = c3.generate({
        bindto: '#SDActual',
        data: {
            columns: [
               actual
            ],
             colors: {
                Actual: "#29AFDF"
            }
        },
        axis: {
            x: {
                type: 'category',
                categories: actualDate,
                tick: {
                    multiline: false,
                    culling: {
                        max: 5
                    }
                }
            }
        },
        zoom: {
            enabled: true,
            rescale: true,
            onzoomend: function(d){
        		chart2.zoom(d);
                chart3.zoom(d);
                chart4.zoom(d);
                chart5.zoom(d);
            }
        },
        legend: {
            position: 'right'
        }
    });
    //MAKE SURE YOU DO THIS LINE FOR ALL CHARTS. YOU MUST CHANGE THE 'type' KEY TO THE TYPE OF GRAPH YOU ARE USING
    charts.push({'chart': chart1, 'type': "SD"})
    
    var chart2 = c3.generate({
        bindto: '#SDTrend',
        data: {
            columns: [
               SDTrend
            ],
             colors: {
                SDTrend: "#ED2835"
            }
        },
        axis: {
            x: {
                type: 'category',
                categories: actualDate,
                tick: {
                    multiline: false,
                    culling: {
                        max: 5
                    }
                }
            }
        },
        zoom: {
            enabled: true,
            rescale: true,
            onzoomend: function(d){
        		chart1.zoom(d);
                chart3.zoom(d);
                chart4.zoom(d);
                chart5.zoom(d);
            }
        },
        legend: {
            position: 'right'
        }
    });
    //MAKE SURE YOU DO THIS LINE FOR ALL CHARTS. YOU MUST CHANGE THE 'type' KEY TO THE TYPE OF GRAPH YOU ARE USING
    charts.push({'chart': chart2, 'type': "SD"})
    
    var chart3 = c3.generate({
        bindto: '#SDSeasonal',
        data: {
            columns: [
               SDSeasonal
            ],
             colors: {               
                SDSeasonal: "#ffa500"
             }
        },
        axis: {
            x: {
                type: 'category',
                categories: actualDate,
                tick: {
                    multiline: false,
                    culling: {
                        max: 5
                    }
                }
            }
        },
        grid: {
            y: {
                lines: [
                    {value: 0}
                ]
            }
        },
        zoom: {
            enabled: true,
            rescale: true,
            onzoomend: function(d){
        		chart1.zoom(d);
                chart2.zoom(d);
                chart4.zoom(d);
                chart5.zoom(d);
            }
        },
        legend: {
            position: 'right'
        }
    });
    charts.push({'chart': chart3, 'type': "SD"})
    
    var chart4 = c3.generate({
        bindto: '#SDResidual',
        data: {
            columns: [
               SDResidual
            ],
             colors: {
                SDResidual: "#d4899c"
            },
            type: 'bar'
        },
        axis: {
            x: {
                type: 'category',
                categories: actualDate,
                tick: {
                    multiline: false,
                    culling: {
                        max: 5
                    }
                }
            }
        },
        grid: {
            y: {
                lines: [
                    {value: 0}
                ]
            }
        },
        bar: {
            width: {
            ratio: .75 // this makes bar width 50% of length between ticks
            }
        },
        zoom: {
            enabled: true,
            rescale: true,
            onzoomend: function(d){
        		chart1.zoom(d);
                chart2.zoom(d);
                chart3.zoom(d);
                chart5.zoom(d);
            }
        },
        legend: {
            position: 'right'
        }
    });
    //MAKE SURE YOU DO THIS LINE FOR ALL CHARTS. YOU MUST CHANGE THE 'type' KEY TO THE TYPE OF GRAPH YOU ARE USING
    charts.push({'chart': chart4, 'type': "SD"})
    
    var chart5 = c3.generate({
        bindto: '#SDCOMBO',
        data: {
            columns: [
                SDResidual,
                SDTrend,
                SDSeasonal,
                actual,
            ],
             colors: {
                Actual: "#29AFDF",
                SDTrend: "#ED2835",
                SDSeasonal: "#ffa500",
                SDResidual: "#d4899c"
            },
            types: {
                actual: 'line',
                SDTrend: 'line',
                SDSeasonal: 'line',
                SDResidual: 'bar',
            },

        },
        axis: {
            x: {
                type: 'category',
                categories: actualDate,
                tick: {
                    multiline: false,
                    culling: {
                        max: 15
                    }
                }
            }
        },
        bar: {
            width: {
            ratio: .4 // this makes bar width 50% of length between ticks
            }
        },
        grid: {
            y: {
                lines: [
                    {value: 0}
                ]
            }
        },
        zoom: {
            enabled: true,
            rescale: true,
            onzoomend: function(d){
        		chart1.zoom(d);
                chart2.zoom(d);
                chart3.zoom(d);
                chart4.zoom(d);
            }
        },
        subchart: {
            show: true,
            onbrush: function (d) {
                chart1.zoom(d);
                chart2.zoom(d);
                chart3.zoom(d);
                chart4.zoom(d);
            },
        },
        legend: {
            position: 'right'
        }
    });
    //MAKE SURE YOU DO THIS LINE FOR ALL CHARTS. YOU MUST CHANGE THE 'type' KEY TO THE TYPE OF GRAPH YOU ARE USING
    charts.push({'chart': chart5, 'type': "SDCombo"})
}

function createResidualGraph(actual, predicted, actualDate) {
    var residual = ["Residual"]
    
    //this section puts NaN in the residual array if the value from the predicted array is "nan". it puts the actual residual otherwise
    for(var i = 1; i < actual.length; i++) {
        a = actual[i]
        p = parseInt(predicted[i])
        
        if (isNaN(p))
            residual.push(NaN)
        else
            residual.push(a - p)
            }
    
    var chart = c3.generate({
        bindto: '#Residual',
        data: {
            columns: [
               residual
            ],
            colors: {
                Residual: "#29AFDF"
            },
            type: 'bar',
        },
        subchart: {
            show: true
        },
        axis: {
            x: {
                type: 'category',
                categories: actualDate,
                tick: {
                    multiline: false,
                    culling: {
                        max: 15
                    }
                },
                label: {
                text: 'Time Series',
                position: 'outer-center'
                }
            },
            y: {
                label: {
                    text: "Values",
                    position: 'outer-middle'

                }
            }
        },
        bar: {
            width: {
            ratio: .75 // this makes bar width 50% of length between ticks
            }
        },
        zoom: {
            enabled: true,
            rescale: true
        },
        legend: {
            position: 'right'
        },
        grid: {
            y: {
                lines: [
                    {value: 0}
                ]
            }
        }
    });
    //MAKE SURE YOU DO THIS LINE FOR ALL CHARTS. YOU MUST CHANGE THE 'type' KEY TO THE TYPE OF GRAPH YOU ARE USING
    charts.push({'chart': chart, 'type': "Residual"})
    
    
}