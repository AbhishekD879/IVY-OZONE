import { Injectable } from '@angular/core';
import * as _ from 'underscore';
import { commandApi } from './command-api.constant';

@Injectable({
  providedIn: 'root'
})
export class CommandService {
    private commands: { [key: string]: any } = {};

    /**
     * Checks is value Promise
     * @param {*} value
     * @returns {boolean}
     */
    static isPromise(value): boolean {
        return !!(value && value.then);
    }

    /**
     * Get error dictionary
     * @return {}
     * @constructor
     */
    static get ERROR(): { [key: string]: string } {
        return {
            ASYNC_COMMAND_MISSED: 'Not existed asynchronous command: ',
            SYNC_COMMAND_MISSED: 'Not existed synchronous command: ',
            COMMAND_NOT_FOUND: 'Not found command to delete: ',
            NOT_PROMISE_RESULT: 'Promise should be returned in command: ',
            PROMISE_RESULT: 'Not a Promise should be returned in command: ',
            COMMAND_OVERRIDE: 'Should no override existed command: '
        };
    }
static set ERROR(value:{ [key: string]: string }){}
    /**
     * Get available APIs which command can execute
     * @constructor
     */
    get API(): { [key: string]: string } {
        return commandApi;
    }
set API(value:{ [key: string]: string }){}
    /**
     * Lazy-load (if not yet) required module,
     * call asynchronous command and receive promise with possible result
     *
     * @param {string} command
     * @param {[*]} [commandFunctionArguments]
     * @param {*} [defaultResult]
     * @returns {Promise.<*>}
     */
    executeAsync(command: string, commandFunctionArguments: Array<any> = [], defaultResult?: any) {
        return this.commands[this.API.LAZY_LOAD](command).then(() => {
            const commandFunction = this.commands[command];

            if (!commandFunction) {
                if (_.isUndefined(defaultResult)) {
                    return Promise.reject(`${CommandService.ERROR.ASYNC_COMMAND_MISSED}${command}`);
                }
                return Promise.resolve(defaultResult);
            }

            const result = commandFunction(...commandFunctionArguments);

            if (!CommandService.isPromise(result)) {
                return Promise.reject(`${CommandService.ERROR.NOT_PROMISE_RESULT}${command}`);
            }

            return result;
        });
    }

    /**
     * Call synchronous command and receive execution result
     * This method is deprecated please use `executeAsync`
     *
     * @params {string} command
     * @params {[*]} [commandFunctionArguments]
     * @params {*} [defaultResult]
     * @returns {any}
     */
    execute(command: string, commandFunctionArguments: Array<any> = [], defaultResult?: any) {
        const commandFunction = this.commands[command];

        if (!commandFunction) {
            if (_.isUndefined(defaultResult)) {
                console.error(`${CommandService.ERROR.SYNC_COMMAND_MISSED}${command}`);
                return null;
            }
            return defaultResult;
        }

        const result = commandFunction(...commandFunctionArguments);

        if (CommandService.isPromise(result)) {
            console.error(`${CommandService.ERROR.PROMISE_RESULT}${command}`);
            return null;
        }

        return result;
    }

    /**
     * Set command function
     * @params {string} command
     * @params {function} commandFunction
     */
    register(command: string, commandFunction: Function) {
        if (this.commands[command]) {
            return;
        }

        this.commands[command] = commandFunction;
    }

    /**
     * @description Remove command
     * @params {string} command
     */
    unregister(command: string) {
        if (!this.commands[command]) {
            console.error(`${CommandService.ERROR.COMMAND_NOT_FOUND}${command}`);
            return;
        }

        delete this.commands[command];
    }
}
