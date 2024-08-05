const setDatePicker = (web_element, date) => {
    // Create a new 'change' event
    let event = new Event('change');
    // Set Date
    const newDate = new Date(date);
    let day = newDate.getDate(); // Use getDate() instead of getDay()
    let month = newDate.getMonth() + 1; // Add 1 because months are 0-indexed
    let year = newDate.getFullYear();
    // Pad the month and day with leading zero if they are less than 10
    const modifiedDate = `${year}-${month < 10 ? `0${month}` : month}-${day < 10 ? `0${day}` : day}`;
    web_element.value = modifiedDate;
    // Dispatch it
    web_element.dispatchEvent(event);
};

setDatePicker(arguments[0], arguments[1]);