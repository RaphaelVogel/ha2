sap.ui.controller("haui.area.solar.Solar", {
	onInit: function() {
	},
	
	handleRefreshPress: function(oEvent){
		var solarModel = sap.ui.getCore().getModel("solarModel");
		solarModel.loadData("/solar/currentData");
	},
	
	handleChartDisplay: function(oEvent){
		sap.ui.getCore().getEventBus().publish("nav", "to", {id : "SolarChart", viewname: 'haui.area.solar.SolarChart'});
	},

	handleNavButtonPress: function(oEvent) {
		sap.ui.getCore().getEventBus().publish("nav", "back");
	}

});