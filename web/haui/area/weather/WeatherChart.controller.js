sap.ui.controller("haui.area.weather.WeatherChart", {

	onInit: function() {

	},

	handleNavButtonPress: function(oEvent) {
		sap.ui.getCore().getEventBus().publish("nav", "back");
	}

});