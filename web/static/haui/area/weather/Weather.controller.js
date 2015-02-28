sap.ui.controller("haui.area.weather.Weather", {
	onInit: function() {
	},
	
	handleRefreshPress: function(oEvent){
		var weatherModel = sap.ui.getCore().getModel("weatherModel");
		weatherModel.loadData("/weather/currentData");
	},
	
	handleNavButtonPress: function(oEvent) {
		sap.ui.getCore().getEventBus().publish("nav", "back");
	},
	
	handleLinePress: function(oEvent) {
		sap.ui.getCore().getEventBus().publish("nav", "to", {id : "WeatherChart", viewname: 'haui.area.weather.WeatherChart', customData: oEvent.getSource().getId()});
	}
});