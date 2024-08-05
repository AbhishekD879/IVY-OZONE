const PropertiesReader = require('properties-reader');
const request = require('sync-request');
const sleep = require('sleep');

const properties = PropertiesReader('.scannerwork/report-task.txt');

const token = 'Basic ' + Buffer.from('a884e07390edf253de28a9592f7624cb3969d793:').toString('base64');

const options = {
    headers: {'Authorization': token}
};

do {
    const body = JSON.parse(request('GET', properties.get('ceTaskUrl'), {
        headers: {
            'Authorization': token
        }
    }).getBody());
    console.log(body);
    if (body.task.status === 'SUCCESS') {
        process.exit(0)
    }
    if (body.task.status === 'FAILED') {
        process.exit(-1)
    }
    sleep.sleep(5);
} while(true);