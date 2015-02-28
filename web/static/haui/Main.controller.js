sap.ui.controller("haui.Main", {
	onInit: function() {
		// Set up navigation handling
		var oBus = sap.ui.getCore().getEventBus();
		oBus.subscribe("nav", "to", this.navToHandler, this);
		oBus.subscribe("nav", "back", this.navBackHandler, this);

		// load weather model for tile
		var weatherTile = this.getView().byId("Weather");
		var weatherModel = new sap.ui.model.json.JSONModel();
		weatherModel.loadData("/weather/currentData");
		sap.ui.getCore().setModel(weatherModel, "weatherModel");
        weatherModel.attachRequestCompleted(function(){
            weatherTile.setInfo("Status: OK");
            weatherTile.setInfoState("Success");
        });
        weatherModel.attachRequestFailed(function(){
			var weatherModel = sap.ui.getCore().getModel("weatherModel");
			var weatherData = {
				"temperature" : "-", "temperatureUnit": "",
				"humidity" : "-", "humidityUnit" : "",
				"pressure" : "-", "pressureUnit" : ""
			};
			weatherModel.setData(weatherData);
			weatherTile.setInfo("Keine Verbindung");
            weatherTile.setInfoState("Error");
        });        
		
		// load solar model for tile
		var solarTile = this.getView().byId("Solar");
        var solarModel = new sap.ui.model.json.JSONModel();
		solarModel.loadData("/solar/currentData");
		sap.ui.getCore().setModel(solarModel, "solarModel");
        solarModel.attachRequestCompleted(function(){
            solarTile.setInfo("Status: OK");
            solarTile.setInfoState("Success");
        });
        solarModel.attachRequestFailed(function(){
			var solarModel = sap.ui.getCore().getModel("solarModel");
			var solarData = {
				"current": "-", "currentUnit": "",
				"day": "-", "dayUnit": "",
				"month": "-", "monthUnit": "",
				"year": "-", "yearUnit": "",
				"total": "-", "totalUnit": ""
			};
			solarModel.setData(solarData);
            solarTile.setInfo("Nicht in Betrieb");
            solarTile.setInfoState("Error");
        });
	},

	navToHandler : function(channelId, eventId, data) {
		var mainView = this.getView();
		var haApp = mainView.byId("haapp");
		var page = haApp.getPage(data.id)
		if(!page){
			page = sap.ui.xmlview(data.id, data.viewname);
			haApp.addPage(page);
		}
		if (data.customData){
			haApp.to(page, {"customData":data.customData});
		} else{
			haApp.to(page);
		}
		
	},

	navBackHandler : function(channelId, eventId, data) {
		var mainView = this.getView();
		var haApp = mainView.byId("haapp");
		haApp.back();
	},

	handleRefreshPress: function(oEvent){
		var weatherModel = sap.ui.getCore().getModel("weatherModel");
		weatherModel.loadData("/weather/currentData");
		var solarModel = sap.ui.getCore().getModel("solarModel");
		solarModel.loadData("/solar/currentData");
	},
	
	handleWeatherPress: function(oEvent) {
		sap.ui.getCore().getEventBus().publish("nav", "to", {id : 'Weather', viewname: 'haui.area.weather.Weather'});
	},
	
	handleHomeControlPress: function(oEvent) {
		sap.ui.getCore().getEventBus().publish("nav", "to", {id : 'HomeControl', viewname: 'haui.area.home.HomeControl'});
	},

	handleSolarPress: function(oEvent) {
		sap.ui.getCore().getEventBus().publish("nav", "to", {id : 'Solar', viewname: 'haui.area.solar.Solar'});
	},

	handleAlarmPress: function(oEvent) {
		sap.ui.getCore().getEventBus().publish("nav", "to", {id : 'Alarm', viewname: 'haui.area.alarm.Alarm'});
	}
});