import json
import requests

solar_data = {
    "current": "5.48",
    "currentUnit": "kW",
    "day": "7.05",
    "dayUnit": "kWh",
    "month": "34.54",
    "monthUnit": "kWh",
    "year": "10.10",
    "yearUnit": "MWh",
    "total": "31.10",
    "totalUnit": "MWh"
}

def read_data(fake=None):
	if fake:
		return json.dump(solar_data)
	try:
		resp = requests.get('http://192.168.1.19/data/ajax.txt?CAN=1&HASH=00100401&TYPE=5', 
			headers={'Accept':'*/*'}, auth=('customer', '********'), timeout=3)
	except
		
	
		
    }, function(err, response, body){
            if(err){
                logger.info("Solar inverter could not be reached.");
                cb("Could not read data from solar inverter: "+err);
                return;
            }
            logger.verbose("Response from solar inverter: "+body);
            /* example body
            master;5.47 kW;5.47 kVA;0.00 kvar;7.05 kWh;7.05 kVAh;0.00 kvarh;34.54 kWh;34.54 kVAh;0.00 kvarh;10.10 MWh;10.10 MVAh;0.00 Mvarh;31.10 MWh;31.10 MVAh;0.00 Mvarh;
            1;AT 5000;2.91 kW;4.1 kWh;16.44 MWh;0055A1701029;268435492;3;00100401;0
            2;NT 4200;2.53 kW;3.4 kWh;14.66 MWh;0044A0313104;268435492;3;00200402;0
            */
            var arr = body.split(";");
            if(arr[0] !== "master" || arr[17] !== "AT 5000"){
                logger.verbose("Incorrect data format from solar inverter");
                cb("Incorrect data format from solar inverter");
                return;
            }
            var currentData = arr[1].split(" ");
            solarData.current = currentData[0];
            solarData.currentUnit = currentData[1];
            var dayData = arr[4].split(" ");
            solarData.day = dayData[0];
            solarData.dayUnit = dayData[1];
            var monthData = arr[7].split(" ");
            solarData.month = monthData[0];
            solarData.monthUnit = monthData[1];
            var yearData = arr[10].split(" ");
            solarData.year = yearData[0];
            solarData.yearUnit = yearData[1];
            var totalData = arr[13].split(" ");
            solarData.total = totalData[0];
            solarData.totalUnit = totalData[1];
            logger.verbose("JSON created from solar inverter response: "+solarData);
            cb(null, solarData);
        }
    );
}

