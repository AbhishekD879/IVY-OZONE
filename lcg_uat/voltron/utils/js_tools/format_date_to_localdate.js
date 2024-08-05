
function convertTo12HourFormat(hour) {
    /**
     * Convert hour from 24-hour format to 12-hour format.
     *
     * @param {number} hour - Hour in 24-hour format (0-23).
     * @returns {Object} - An object containing hour in 12-hour format and clock cycle (AM/PM).
     */
    let clockCycle = 'AM';
    if (hour === 0) {
        hour = 12;
    } else if (hour === 12) {
        clockCycle = 'PM';
    } else if (hour > 12) {
        hour -= 12;
        clockCycle = 'PM';
    }
    return { hour: hour.toString(), clockCycle: clockCycle };
}

function formatDate(utcDateString,format,hour12=false) {
    const MONTH_MAP = {
        "01": "Jan",
        "02": "Feb",
        "03": "Mar",
        "04": "Apr",
        "05": "May",
        "06": "Jun",
        "07": "Jul",
        "08": "Aug",
        "09": "Sep",
        "10": "Oct",
        "11": "Nov",
        "12": "Dec"
    };
    const date = new Date(utcDateString);
    const options = {
     weekday:"long",
     year:"numeric",
     month:"2-digit", // month in number format,
     day:"2-digit",
     hour:"2-digit",
     minute:"2-digit",
     second:"2-digit",
    };

    // Format the date
    const trim = el => el.trim();
    const convertedDate = date.toLocaleString('en-GB', options)?.split(',').map(trim);
    console.log(convertedDate + "Date")
    const [day,dateParts,time] = convertedDate;
    const [DD,MM,YYYY] = dateParts?.split("/").map(trim);
    let [HH,MIN,SS] = time.split(":").map(trim);
    if(hour12){
        const convertedTime = convertTo12HourFormat(HH);
        HH = convertedTime.hour;
        format = format.replaceAll("AM/PM",convertedTime.clockCycle)
    }else{
        format = format.replaceAll("AM/PM","");
    }
    format = format.replaceAll("MM",MM)
    format = format.replaceAll("DD",DD)
    format = format.replaceAll("YYYY",YYYY)
    format = format.replaceAll("DAY",day)
    format = format.replaceAll("HH",HH)
    format = format.replaceAll("MIN",MIN)
    format = format.replaceAll("SS",SS)
    format = format.replaceAll("MON|STR",MONTH_MAP[MM])
    return format
}
return formatDate(...arguments)