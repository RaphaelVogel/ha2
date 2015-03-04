sap.ui.controller("haui.area.solar.SolarChart", {
    year: new Date().getFullYear(),
	month: new Date().getMonth() + 1,

    onInit: function() {
		var that = this;
		if(this.month < 10){
			this.month = "0"+this.month;
		}
		this.getView().byId("allSelected").setText("Alle Jahre");
		this.getView().byId("yearSelected").setText(this.year);
		this.getView().byId("monthSelected").setText(haui.Util.numberToMonth(this.month.toString()));
        var solarChartModel = new sap.ui.model.json.JSONModel();
        this.getView().byId("solarChart").setModel(solarChartModel);

        this.getView().addEventDelegate({
            // call every time when page is displayed
            onBeforeShow: function(evt) {
                var solarChart = this.getView().byId("solarChart");
				this.getView().byId("selectBox").setSelectedKey("monthSelected");
                var solarChartModel = this.getView().byId("solarChart").getModel();
                this.getView().byId("solarChartPage").setTitle("Produktion im "+haui.Util.numberToMonth(this.month.toString()));
                solarChartModel.loadData("/solar/historicProduction?year="+this.year+"&month="+this.month);
            }
        }, this);

    },

	// called if user changes dropdown box
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
		}
	},

	handleAllPress: function(){
		var solarChartModel = this.getView().byId("solarChart").getModel();
        this.getView().byId("solarChartPage").setTitle("Produktion aller Jahre");
        solarChartModel.loadData("/solar/historicProduction");
	},

	handleYearPress: function(oEvent){
		var solarChartModel = this.getView().byId("solarChart").getModel();
        this.getView().byId("solarChartPage").setTitle("Produktion "+this.year);
        solarChartModel.loadData("/solar/historicProduction?year="+this.year);
	},

	handleMonthPress: function(oEvent){
		var solarChartModel = this.getView().byId("solarChart").getModel();
        this.getView().byId("solarChartPage").setTitle("Produktion "+haui.Util.numberToMonth(this.month.toString())+" "+this.year);
        solarChartModel.loadData("/solar/historicProduction?year="+this.year+"&month="+this.month);
	},

	// User double clicks on one value
	chartPressed: function(oEvent){
		var category = this.getView().byId("solarChart").getSelectedCategory();
		var solarChartModel = this.getView().byId("solarChart").getModel();
        if(category && category.indexOf(':') == -1){
			if(category.length === 4){
				// year selected e.g. 2014
                this.getView().byId("solarChartPage").setTitle("Produktion "+category);
                this.getView().byId("selectBox").setSelectedKey("nothingSelected");
                solarChartModel.loadData("/solar/historicProduction?year="+category);
			}
			else if(category.length === 7){
				// month selected e.g. 12 2014
				var splitDate = category.split(' ');
                this.getView().byId("solarChartPage").setTitle("Produktion "+haui.Util.numberToMonth(splitDate[0])+" "+splitDate[1]);
                this.getView().byId("selectBox").setSelectedKey("nothingSelected");
                solarChartModel.loadData("/solar/historicProduction?year="+splitDate[1]+"&month="+splitDate[0]);
			}
		}
	},

	handleNavButtonPress: function(oEvent) {
		sap.ui.getCore().getEventBus().publish("nav", "back");
	}

});