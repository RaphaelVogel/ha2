sap.ui.controller("haui.area.weather.Weather", {
	onInit: function() {
	},
	
	handleRefreshPress: function(oEvent){
		var weatherModel = sap.ui.getCore().getModel("weatherModel");
		weatherModel.loadData("/weather/current");
	},
	
	handleNavButtonPress: function(oEvent) {
		sap.ui.getCore().getEventBus().publish("nav", "back");
	},
	
	handleTempPress: function(oEvent) {
		sap.ui.getCore().getEventBus().publish("nav", "to", {id : "TempChart", viewname: 'haui.area.weather.TempChart'});
	},

	handleHumidityPress: function(oEvent) {
		sap.ui.getCore().getEventBus().publish("nav", "to", {id : "HumidityChart", viewname: 'haui.area.weather.HumidityChart'});
	},

	handlePressurePress: function(oEvent) {
		sap.ui.getCore().getEventBus().publish("nav", "to", {id : "PressureChart", viewname: 'haui.area.weather.PressureChart'});
	}
});