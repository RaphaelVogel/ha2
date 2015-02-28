sap.ui.controller("haui.area.weather.WeatherChart", {
    year: new Date().getFullYear(),
	month: new Date().getMonth() + 1,
	day: new Date().getDate(),
	displayData: "", //Weather--temperatureData, Weather--humidityData, Weather--pressureData
	
	onInit: function() {
		var that = this;
        if(this.day < 10){
			this.day = "0"+this.day;
		}
		if(this.month < 10){
			this.month = "0"+this.month;
		}		
		this.getView().byId("allSelected").setText("Alle Jahre");
		this.getView().byId("yearSelected").setText(this.year);
		this.getView().byId("monthSelected").setText(haui.Util.numberToMonth(this.month.toString()));
		this.getView().byId("daySelected").setText("Heute");		
        var weatherChartModel = new sap.ui.model.json.JSONModel();
        this.getView().byId("weatherChart").setModel(weatherChartModel);
        this.getView().addEventDelegate({
            // call every time when page is displayed
            onBeforeShow: function(evt) {
                this.displayData = evt.data.customData;
                var weatherChart = this.getView().byId("weatherChart");
                weatherChart.setType("Line");
				this.getView().byId("selectBox").setSelectedKey("monthSelected");
                var weatherChartModel = this.getView().byId("weatherChart").getModel();
				if(this.isTemperatureChart()){
                    this.getView().byId("weatherChartPage").setTitle("Temperatur im "+haui.Util.numberToMonth(this.month.toString()));
                    weatherChart.getValues()[0].setDisplayName("Temperatur C°");
                    weatherChartModel.loadData("/weather/historicTemperatures?year="+this.year+"&month="+this.month); 
                }
                else if(this.isHumidityChart()){
                    this.getView().byId("weatherChartPage").setTitle("Luftfeuchtigkeit im "+haui.Util.numberToMonth(this.month.toString()));
                    weatherChart.getValues()[0].setDisplayName("Luftfeuchtigkeit %RH");
                    weatherChartModel.loadData("/weather/historicHumidities?year="+this.year+"&month="+this.month);				
                }
                else if(this.isPressureChart()){
                    this.getView().byId("weatherChartPage").setTitle("Luftdruck im "+haui.Util.numberToMonth(this.month.toString()));
                    weatherChart.getValues()[0].setDisplayName("Luftdruck mBar");
                    weatherChartModel.loadData("/weather/historicPressures?year="+this.year+"&month="+this.month);				
                }
            }
        }, this);
        weatherChartModel.attachRequestCompleted(function(req){
            if(req.getParameters().url.indexOf("historicTemperatures") > -1){
                that.getView().byId("weatherChart").getValueAxis()
                .setMin((that.getView().byId("weatherChart").getModel().getProperty("/minrange")).toString())
                .setMax((that.getView().byId("weatherChart").getModel().getProperty("/maxrange")).toString());
            }
            else if(req.getParameters().url.indexOf("historicHumidities") > -1){
                that.getView().byId("weatherChart").getValueAxis()
                .setMin((that.getView().byId("weatherChart").getModel().getProperty("/minrange")).toString())
                .setMax("100");
            }
            else if(req.getParameters().url.indexOf("historicPressures") > -1){
                that.getView().byId("weatherChart").getValueAxis()
                .setMin((that.getView().byId("weatherChart").getModel().getProperty("/minrange")).toString())
                .setMax((that.getView().byId("weatherChart").getModel().getProperty("/maxrange")).toString());
            }
        }); 
	},
	
	handleSelectPress: function(){
		var key = this.getView().byId("selectBox").getSelectedKey();
		switch(key){
		case "allSelected":
			this.handleAllPress();
			break;
		case "yearSelected":
			this.handleYearPress();
			break;
		case "monthSelected":
			this.handleMonthPress();
			break;
		case "daySelected":
			this.handleDayPress();
			break;
		}
	},
	
	handleAllPress: function(){
		this.getView().byId("weatherChart").setType("Column");
		var weatherChartModel = this.getView().byId("weatherChart").getModel();
		if(this.isTemperatureChart()){
            this.getView().byId("weatherChartPage").setTitle("Temperatur aller Jahre");
            weatherChartModel.loadData("/weather/historicTemperatures");            
		}
		else if(this.isHumidityChart()){
            this.getView().byId("weatherChartPage").setTitle("Luftfeuchte aller Jahre");
			weatherChartModel.loadData("/weather/historicHumidities");
		}
		else if(this.isPressureChart()){
            this.getView().byId("weatherChartPage").setTitle("Luftdruck aller Jahre");
			weatherChartModel.loadData("/weather/historicPressures");
		}	
	},
	
	handleYearPress: function(oEvent){
		this.getView().byId("weatherChart").setType("Line");
		var weatherChartModel = this.getView().byId("weatherChart").getModel();
		if(this.isTemperatureChart()){
            this.getView().byId("weatherChartPage").setTitle("Temperatur "+this.year);
			weatherChartModel.loadData("/weather/historicTemperatures?year="+this.year);
		}
		else if(this.isHumidityChart()){
            this.getView().byId("weatherChartPage").setTitle("Luftfeuchte "+this.year);
			weatherChartModel.loadData("/weather/historicHumidities?year="+this.year);
		}
		else if(this.isPressureChart()){
            this.getView().byId("weatherChartPage").setTitle("Luftdruck "+this.year);
			weatherChartModel.loadData("/weather/historicPressures?year="+this.year);
		}
	},

	handleMonthPress: function(oEvent){
		this.getView().byId("weatherChart").setType("Line");
		var weatherChartModel = this.getView().byId("weatherChart").getModel();
		if(this.isTemperatureChart()){
            this.getView().byId("weatherChartPage").setTitle("Temperatur "+haui.Util.numberToMonth(this.month.toString())+" "+this.year);
			weatherChartModel.loadData("/weather/historicTemperatures?year="+this.year+"&month="+this.month);	
		}
		else if(this.isHumidityChart()){
            this.getView().byId("weatherChartPage").setTitle("Luftfeuchte "+haui.Util.numberToMonth(this.month.toString())+" "+this.year);
			weatherChartModel.loadData("/weather/historicHumidities?year="+this.year+"&month="+this.month);
		}
		else if(this.isPressureChart()){
            this.getView().byId("weatherChartPage").setTitle("Luftdruck "+haui.Util.numberToMonth(this.month.toString())+" "+this.year);
			weatherChartModel.loadData("/weather/historicPressures?year="+this.year+"&month="+this.month);
		}
	},

	handleDayPress: function(oEvent){
		this.getView().byId("weatherChart").setType("Line");
		var weatherChartModel = this.getView().byId("weatherChart").getModel();
		if(this.isTemperatureChart()){
            this.getView().byId("weatherChartPage").setTitle("Temperatur am "+this.day+". "+haui.Util.numberToMonth(this.month.toString())+" "+this.year);
            weatherChartModel.loadData("/weather/historicTemperatures?year="+this.year+"&month="+this.month+"&day="+this.day);
		}
		else if(this.isHumidityChart()){
            this.getView().byId("weatherChartPage").setTitle("Luftfeuchte am "+this.day+". "+haui.Util.numberToMonth(this.month.toString())+" "+this.year);
			weatherChartModel.loadData("/weather/historicHumidities?year="+this.year+"&month="+this.month+"&day="+this.day);
		}
		else if(this.isPressureChart()){
            this.getView().byId("weatherChartPage").setTitle("Luftdruck am "+this.day+". "+haui.Util.numberToMonth(this.month.toString())+" "+this.year);
			weatherChartModel.loadData("/weather/historicPressures?year="+this.year+"&month="+this.month+"&day="+this.day);
		}
	},
	
	chartPressed: function(oEvent){
		var category = this.getView().byId("weatherChart").getSelectedCategory();
		var weatherChartModel = this.getView().byId("weatherChart").getModel();
        if(category && category.indexOf(':') == -1){
            this.getView().byId("weatherChart").setType("Line");
			if(category.length === 4){
				// year selected e.g. 2014
				if(this.isTemperatureChart()){
                    this.getView().byId("weatherChartPage").setTitle("Temperatur "+category);
					this.getView().byId("selectBox").setSelectedKey("nothingSelected");
                    weatherChartModel.loadData("/weather/historicTemperatures?year="+category);
                }
                else if(this.isHumidityChart()){
                    this.getView().byId("weatherChartPage").setTitle("Luftfeuchte "+category);
					this.getView().byId("selectBox").setSelectedKey("nothingSelected");
                    weatherChartModel.loadData("/weather/historicHumidities?year="+category);
                }
                else if(this.isPressureChart()){
                    this.getView().byId("weatherChartPage").setTitle("Luftdruck "+category);
					this.getView().byId("selectBox").setSelectedKey("nothingSelected");
                    weatherChartModel.loadData("/weather/historicPressures?year="+category);
                }
			}
			else if(category.length === 7){
				// month selected e.g. 12 2014
				var splitDate = category.split(' ');
                if(this.isTemperatureChart()){
                    this.getView().byId("weatherChartPage").setTitle("Temperatur "+haui.Util.numberToMonth(splitDate[0])+" "+splitDate[1]);
					this.getView().byId("selectBox").setSelectedKey("nothingSelected");
                    weatherChartModel.loadData("/weather/historicTemperatures?year="+splitDate[1]+"&month="+splitDate[0]);
                }
                else if(this.isHumidityChart()){
                    this.getView().byId("weatherChartPage").setTitle("Luftfeuchte "+haui.Util.numberToMonth(splitDate[0])+" "+splitDate[1]);
					this.getView().byId("selectBox").setSelectedKey("nothingSelected");
                    weatherChartModel.loadData("/weather/historicHumidities?year="+splitDate[1]+"&month="+splitDate[0]);
                }
                else if(this.isPressureChart()){
                    this.getView().byId("weatherChartPage").setTitle("Luftdruck "+haui.Util.numberToMonth(splitDate[0])+" "+splitDate[1]);
					this.getView().byId("selectBox").setSelectedKey("nothingSelected");
                    weatherChartModel.loadData("/weather/historicPressures?year="+splitDate[1]+"&month="+splitDate[0]);
                }				
			}
			else if(category.length === 11){
                // day selected e.g. 05.12. 2014
                var splitDate = category.split(' ');
                var splitMonth = splitDate[0].split('.');
                if(this.isTemperatureChart()){
                    this.getView().byId("weatherChartPage").setTitle("Temperatur am "+splitMonth[0]+". "+haui.Util.numberToMonth(splitMonth[1])+" "+splitDate[1]);
					this.getView().byId("selectBox").setSelectedKey("nothingSelected");
                    weatherChartModel.loadData("/weather/historicTemperatures?year="+splitDate[1]+"&month="+splitMonth[1]+"&day="+splitMonth[0]);                    
                }
                else if(this.isHumidityChart()){
                    this.getView().byId("weatherChartPage").setTitle("Luftfeuchte am "+splitMonth[0]+". "+haui.Util.numberToMonth(splitMonth[1])+" "+splitDate[1]);
					this.getView().byId("selectBox").setSelectedKey("nothingSelected");
                    weatherChartModel.loadData("/weather/historicHumidities?year="+splitDate[1]+"&month="+splitMonth[1]+"&day="+splitMonth[0]);
                }
                else if(this.isPressureChart()){
                    this.getView().byId("weatherChartPage").setTitle("Luftdruck am "+splitMonth[0]+". "+haui.Util.numberToMonth(splitMonth[1])+" "+splitDate[1]);
					this.getView().byId("selectBox").setSelectedKey("nothingSelected");
                    weatherChartModel.loadData("/weather/historicPressures?year="+splitDate[1]+"&month="+splitMonth[1]+"&day="+splitMonth[0]);
                }				
			}
		}
	},
	
    isTemperatureChart: function(){
        return (this.displayData === "Weather--temperatureData");
    },
    
    isHumidityChart: function(){
        return (this.displayData === "Weather--humidityData");
    },
    
    isPressureChart: function(){
        return (this.displayData === "Weather--pressureData");
    },    
    
	handleNavButtonPress: function(oEvent) {
		sap.ui.getCore().getEventBus().publish("nav", "back");
	},
    
    getMinMaxForTemperature: function(values){
        var min=0; max=0;
        values.forEach(function(obj){
            if(obj.value > max){
                max = obj.value;
            }
            if(obj.value < min){
                min = obj.value;
            }
        });
        return {"min":min, "max":max};
    }
});