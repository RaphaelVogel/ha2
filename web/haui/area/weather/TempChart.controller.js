sap.ui.controller("haui.area.weather.TempChart", {
    year: new Date().getFullYear(),
	month: new Date().getMonth() + 1,
	day: new Date().getDate(),

	onInit: function() {
	    if(this.day < 10){
		    this.day = "0"+this.day;
		}
		if(this.month < 10){
			this.month = "0"+this.month;
		}
        var tempChart = this.getView().byId("tempChart");
		var tempModel = new sap.ui.model.json.JSONModel();
		tempModel.loadData("/weather/historicTemperatures?year="+this.year+"&month="+this.month)
		sap.ui.getCore().setModel(tempModel, "tempModel");
	},

	handleNavButtonPress: function(oEvent) {
		sap.ui.getCore().getEventBus().publish("nav", "back");
	}

});
