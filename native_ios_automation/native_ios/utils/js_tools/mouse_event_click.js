return arguments[0].dispatchEvent(new MouseEvent('click', {view: window, bubbles:true, cancelable: true}))
