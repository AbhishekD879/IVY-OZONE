export const FORECAST_CONFIG = {
  forecastMarketPath: 'forecast',
  tricastMarketPath: 'tricast',
  poolTypesMap: {
    FC: { name: 'Forecast', path: 'forecast' },
    TC: { name: 'Tricast', path: 'tricast' }
  },
  eventDefaults: {
    INPLAY: 0, //Always 0
    CUSTOMER_BUILT: 0, //Always 0
    MODULE: 'racecard', //Default for forecast/tricast
    ODDSBOOST_VALUE: 0, //Always 0
    STREAM_ACTIVE: 0, //Always 0
    STREAM_ID: null, //Always null
    QUANTITY_VAL: 1 //Always 1
  }
};
