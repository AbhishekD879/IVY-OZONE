export interface ControlParams {
    name: string;
    type: string;
    value: any;
    label: string;
    required?: boolean;
}

export interface DialogOptions {
    width?: string;
    title: string;
    message?: string;
    hint?: string;
    noOption?: string;
    yesOption?: string;
    controls?: ControlParams[];
    closeCallback?: any;
    yesCallback?: any;
    noCallback?: any;
    messagesArray?: string[];
    data?: any;
}
