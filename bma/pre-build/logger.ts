const COLORS = {
  RED: '\x1b[31m%s\x1b[0m',
  YELLOW: '\x1b[33m%s\x1b[0m'
};

export default {
  log(...args: any[]) {    
    print(args, COLORS.YELLOW);
  },
  error(...args: any[]) {
    print(args, COLORS.RED);
  }
};

function print(args, color) {
  const msg = args.map(arg => typeof arg === 'object' ? JSON.stringify(arg) : arg);
  console.log(color, '----------------------------------------------------------\n' + msg.join(', '));
}
