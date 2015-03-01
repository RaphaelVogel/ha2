sap.ui.controller("haui.area.alarm.Alarm", {
	onInit: function() {
	},
    
	handleNavButtonPress: function(oEvent) {
		sap.ui.getCore().getEventBus().publish("nav", "back");
	}

});