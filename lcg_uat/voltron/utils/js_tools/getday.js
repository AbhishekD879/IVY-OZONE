
function formatDate(utcDateString,format) {
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
    const [HH,MIN,SS] = time.split(":").map(trim);
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



function getRelativeDate(utcDateString) {
    const date = new Date(utcDateString);
    const currentDate = new Date();

    // Set both dates to midnight to compare only dates without time
    date.setHours(0, 0, 0, 0);
    currentDate.setHours(0, 0, 0, 0);

    // Calculate the difference in milliseconds between the two dates
    const differenceInMilliseconds = date.getTime() - currentDate.getTime();

    // Calculate the difference in days
    const differenceInDays = Math.floor(differenceInMilliseconds / (1000 * 60 * 60 * 24));

    let relativeDate = '';
    if (differenceInDays === 0) {
        relativeDate = 'Today';
    } else {
        relativeDate = formatDate(utcDateString,'DD MON|STR');
    }

    return relativeDate;
}

return getRelativeDate(arguments[0])