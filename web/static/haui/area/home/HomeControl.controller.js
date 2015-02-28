sap.ui.controller("haui.area.home.HomeControl", {    
    onInit: function() {
        var zwaveModel = new sap.ui.model.json.JSONModel();
        sap.ui.getCore().setModel(zwaveModel, "zwaveModel");
        this.getView().addEventDelegate({
            // call every time when page is displayed
            onBeforeShow: function(evt) {
                this.refreshZWaveState(); 
            }
        }, this);
	},
    
    refreshZWaveState: function(){
        var zwaveModel = sap.ui.getCore().getModel("zwaveModel");
		zwaveModel.loadData("/zwave/state");
    },
	
	handleLivingroomLight: function(oEvent){
		var state = oEvent.getSource().getState();
		state = haui.Util.boolToString(state);
		var getRequest = $.ajax({
			type: 'GET',
			url: "/zwave/livingroomLight/"+state,
			dataType: "json"
		});
	},
	
	handleRefreshPress: function(oEvent){
        this.refreshZWaveState();
	},
	
	handleNavButtonPress: function(oEvent) {
		sap.ui.getCore().getEventBus().publish("nav", "back");
	}

});