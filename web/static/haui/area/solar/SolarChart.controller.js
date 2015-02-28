sap.ui.controller("haui.area.solar.SolarChart", {
    onInit: function() {
        var solarChartModel = new sap.ui.model.json.JSONModel();
        this.getView().byId("solarChart").setModel(solarChartModel);
        this.getView().addEventDelegate({
            // call every time when page is displayed
            onBeforeShow: function(evt) {
                this.refreshSolarData(); 
            }
        }, this);
	},
    
    refreshSolarData: function(){
        var solarChartModel = this.getView().byId("solarChart").getModel();
		solarChartModel.loadData("/solar/historicProductionData");
    },
	
	handleNavButtonPress: function(oEvent) {
		sap.ui.getCore().getEventBus().publish("nav", "back");
	}

});