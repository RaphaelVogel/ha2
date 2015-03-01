jQuery.sap.declare("haui.Util");
jQuery.sap.require("sap.ui.core.format.DateFormat");

haui.Util = {
	stringToBool: function(stringVal){
		if(!stringVal) return;
		if(stringVal === "ON"){
			return true;
		}
		else if(stringVal === "OFF"){
			return false
		}
		else
			return null;
	},
	
	boolToString: function(boolVal){
		if(boolVal === undefined) return;
		if(boolVal === true){
			return "ON";
		}
		else if(boolVal === false){
			return "OFF";
		}
		else
			return null;
	},
    
    numberToMonth: function(number){
        switch(number){
            case "01":
                return "Jan.";
                break;
            case "02":
                return "Feb.";
                break;
            case "03":
                return "März";
                break;
            case "04":
                return "April";
                break;
            case "05":
                return "Mai";
                break;
            case "06":
                return "Juni";
                break;
            case "07":
                return "Juli";
                break;
            case "08":
                return "Aug.";
                break;
            case "09":
                return "Sept.";
                break;
            case "10":
                return "Okt.";
                break;
            case "11":
                return "Nov.";
                break;
            case "12":
                return "Dez.";
                break;
        }
    
    }
};