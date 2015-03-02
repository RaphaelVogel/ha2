sap.ui.controller("haui.area.solar.SolarChart", {
    onInit: function() {

	},
	
	handleNavButtonPress: function(oEvent) {
		sap.ui.getCore().getEventBus().publish("nav", "back");
	}

});