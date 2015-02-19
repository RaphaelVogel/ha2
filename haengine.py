var logger = require('../support/logger');
var CronJob = require('cron').CronJob;
var async = require('async');
var weather = require('../access_modules/weather');
var solar = require('../access_modules/solar');
var sqlite3 = require('sqlite3');


// Weather job
var jobWeather = new CronJob('00 */20 * * * *', function(){ // job starts
    logger.info("Start weather job");
    var db = new sqlite3.Database('../ha.db');
    weather.readWeatherData(function(err, weatherData){
        if(err){
            logger.error("Job could not read weather data from TF");
            return;
        } else{
            logger.verbose("Weather temperature from sensor:"+weatherData.temperature);
            logger.verbose("Weather humidity from sensor:"+weatherData.humidity);
            logger.verbose("Weather pressure from sensor:"+weatherData.pressure);

            // check if temperature change is bigger than 6 C since the last 20 min -> this is an outlier
            db.all("select max(timestamp), val_real from sensordata where device_id = 1 and sensor_id = 1", function(err, rows){
                if(!rows[0].val_real){
                    // first time
                    db.run('INSERT INTO sensordata (device_id, sensor_id, val_real) VALUES (1,1,?)', [ weatherData.temperature ]);
                    return;
                }
                logger.verbose("Last temperature from DB: "+rows[0].val_real);
                if(weatherData.temperature && Math.abs(rows[0].val_real - weatherData.temperature) <= 6){
                    logger.verbose("Insert new temperature value: "+weatherData.temperature);
                    db.run('INSERT INTO sensordata (device_id, sensor_id, val_real) VALUES (1,1,?)', [ weatherData.temperature ]);
                }
                else{
                    logger.warn("Sensor temperature value "+weatherData.temperature+" is to different from DB pressure value "+rows[0].val_real+". Nothing inserted into DB");
                }                 
            });            
            // check if humidity change is bigger than 6 %RH since the last 20 min -> this is an outlier
            db.all("select max(timestamp), val_real from sensordata where device_id = 1 and sensor_id = 2", function(err, rows){
                if(!rows[0].val_real){
                    // first time
                    db.run('INSERT INTO sensordata (device_id, sensor_id, val_real) VALUES (1,2,?)', [ weatherData.humidity ]);
                    return;
                }                
                logger.verbose("Last humidity value from DB: "+rows[0].val_real);
                if(weatherData.humidity && Math.abs(rows[0].val_real - weatherData.humidity) <= 6){
                    logger.verbose("Insert new humidity value: "+weatherData.humidity);
                    db.run('INSERT INTO sensordata (device_id, sensor_id, val_real) VALUES (1,2,?)', [ weatherData.humidity ]);   
                }
                else{
                    logger.warn("Sensor humidity value "+weatherData.humidity+" is to different from DB pressure value "+rows[0].val_real+". Nothing inserted into DB");
                }                
            });
            // check if pressure change is bigger than 3 mBar since the last 20 min -> this is an outlier
            db.all("select max(timestamp), val_real from sensordata where device_id = 1 and sensor_id = 3", function(err, rows){
                if(!rows[0].val_real){
                    // first time
                    db.run('INSERT INTO sensordata (device_id, sensor_id, val_real) VALUES (1,3,?)', [ weatherData.pressure ]);
                    return;
                }                
                logger.verbose("Last pressure value from DB: "+rows[0].val_real);
                if(weatherData.pressure && Math.abs(rows[0].val_real - weatherData.pressure) <= 3){
                    logger.verbose("Insert new pressure value: "+weatherData.pressure);
                    db.run('INSERT INTO sensordata (device_id, sensor_id, val_real) VALUES (1,3,?)', [ weatherData.pressure ]);   
                }
                else{
                    logger.warn("Sensor pressure value "+weatherData.pressure+" is to different from DB pressure value "+rows[0].val_real+". Nothing inserted into DB");
                }
            });            
        }
    });
}, 
function () { // Job has ended
    logger.info("Weather job has ended");
    db.close();
}, true);



// Solar job
var jobSolar = new CronJob('00 30 8 * * *', function(){
    logger.info("Start solar job");
    var db = new sqlite3.Database('../ha.db');
    solar.readData(function(err, solarData){
        if(err){
            logger.error("Job could not read solar data");
            return;
        } else{
            logger.info("Insert the following solar data into DB: "+solarData);
            db.run('INSERT INTO sensordata (device_id, sensor_id, val_real) VALUES (2,1,?)', [ solarData.month ]);
        }        
    })
},
function(){
    logger.info("Solar job has ended");
    db.close();
}, true);



process.on('SIGINT', function() {
  process.exit(0);
});
process.on('SIGTERM', function() {
  process.exit(0);
});
